from app.query.executor.query_executor import QueryEmbedder
from app.query.formatter import create_weaviate_filter
from app.query.query_expanision.classifer import JUNK_WORDS, queryclassifier
from app.query.query_expanision.post_processing import build_query_segments
from traning_data_generation.feature_score_generation import build_features
from app.storage.connections import get_client
from app.query.query_expanision.query_normalizer import clean_query
from collections import defaultdict
import spacy
import pandas as pd
import ast
import json
import os

# queries = [
#     "Buy a House in Colombo",
#     "Hello everyone! I’m looking for a house to buy or land with electricity and water already connected. 📍 Preferred location: Habaraduwa area ➡️ I will also consider properties from Talpe to Ahangama Requirements: • 4–5 bedrooms • 4–5 bathrooms • Maximum 2.5 km from the beach • Clear legal status – I will verify the Title Report with my lawyer.",
#     # "Looking for a 3+ bedroom boutique villa for long term lease. In between galle fort to Thalpe",
#     # "Hi, Im looking for a house to rent in Hiriketya from 1.11.25-1.12.25. I would like a house with a good kitchen, an outside place to sit and a workingplace.",
#     # "Looking for a House for Rent 2 Bedrooms Kitchen Living Room Washroom Parking Preferred Areas: Moratuwa, Panadura, Piliyandala 💰 Budget: Rs. 30,000 – 40,000/-",
#     # "We are looking for a house to rent in Ahangama starting from 21 February for a duration of 2–3 months. The house should have 3 bedrooms and 2 bathrooms, along with a fully equipped kitchen. Air conditioning is required in all bedrooms, and the property should include a living room with a sofa. Ideally, it should also have a small garden and a terrace space. Our budget is up to 350,000 LKR per month. We are a quiet family and will take good care of the house.",
#     # "We are looking for a 3+ bedroom boutique villa for a long-term lease. The preferred location is between Galle Fort and Thalpe. The property should be suitable for long-term living and offer a comfortable and private environment.",
#     # "I am looking for a house to rent in Hiriketiya from 1 November 2025 to 1 December 2025. The house should include a good kitchen, an outdoor seating area, and a workspace suitable for working remotely.",
#     # "I am looking for a house for rent with 2 bedrooms, a kitchen, living room, washroom, and parking space. Preferred locations are Moratuwa, Panadura, or Piliyandala. My budget is between Rs. 30,000 and 40,000 per month.",
#     # "land for sale in Colombo with good access to public transport",
#     # "villa in Galle with pool and sea view for sale",
#     # "affordable house in Kandy with 3 bedrooms and garden for rent",
# ]

nlp = spacy.load(r"D:\FYP\RealSearch\VectorEngine\models\model-best")

queries_path = r"D:\FYP\RealSearch\VectorEngine\query_data\raw_queries.csv"
ground_truth_path = r"D:\FYP\RealSearch\VectorEngine\ground truth\ground_truth_1_10.csv"

results_log = []

output_path = (
    r"D:\FYP\RealSearch\VectorEngine\traning_data_generation\alpha_training_data.csv"
)


def training_data_pipeline_test(query_id, user_query, client, relevant_ids):
    # print(f"\n{'='*60}\nQUERY: {user_query}")

    user_query = clean_query(user_query)
    extraction = entity_extraction(user_query)

    print(f"EXTRACTION: {extraction}")

    features = build_features(user_query, extraction)
    print(f"FEATURES: {features}")

    relevant_ids = [str(x) for x in relevant_ids]

    best_alpha = compute_best_alpha(user_query, client, relevant_ids, k=10)

    print(f"Best Alpha: {best_alpha}")
    # STORE instead of print
    results_log.append(
        {"query_id": query_id, "features": features, "alpha": best_alpha}
    )


def entity_extraction(user_query):
    doc = nlp(user_query)

    raw_entities = defaultdict(list)

    for ent in doc.ents:
        words = ent.text.split()

        # Clean trailing junk words
        if words[-1].lower() in JUNK_WORDS:
            clean_text = " ".join(words[:-1])
        else:
            clean_text = ent.text

        raw_entities[ent.label_].append(clean_text)

    processed = {}

    # Property types (keep all)
    if "property_type" in raw_entities:
        processed["property_type"] = list(set(raw_entities["property_type"]))

    # Locations (keep all)
    if "location" in raw_entities:
        processed["location"] = list(set(raw_entities["location"]))

    for slot in [
        "property_type",
        "contract_type",
        "location",
        "no_of_bedrooms",
        "no_of_bathrooms",
        "price",
        "land_size",
    ]:
        if slot in raw_entities:
            processed[slot] = list(set(raw_entities[slot]))

    return processed


import numpy as np


def compute_ndcg(retrieved_ids, relevant_ids, k=10):
    dcg = 0.0

    for i, doc_id in enumerate(retrieved_ids[:k]):
        if doc_id in relevant_ids:
            dcg += 1 / np.log2(i + 2)

    ideal_hits = min(len(relevant_ids), k)
    idcg = sum(1 / np.log2(i + 2) for i in range(ideal_hits))

    if idcg == 0:
        return 0.0

    return dcg / idcg


def run_hybrid_search(user_query, client, alpha, k=10):

    classification = queryclassifier(user_query)
    entities = classification["entities"]
    # print(f"Extracted Entities: {entities}")

    # result_segment = build_query_segments(user_query, entities)

    embedder = QueryEmbedder()
    query_vector = embedder.get_vector(user_query)

    # wv_filter = create_weaviate_filter(result_segment)

    properties = client.collections.get("RealSearchPropData1")

    results = properties.query.hybrid(
        query=user_query,
        vector=query_vector,
        # filters=wv_filter,
        alpha=alpha,
        limit=k,
    )

    retrieved_ids = []

    if getattr(results, "objects", None):
        for obj in results.objects:
            p = obj.properties
            retrieved_ids.append(p.get("propertyId"))  # IMPORTANT: use unique id field

    return retrieved_ids


def compute_best_alpha(query, client, relevant_ids, k=10):
    alphas = [0.0, 0.25, 0.5, 0.75, 1.0]
    ndcg_scores = []

    for alpha in alphas:
        retrieved_ids = run_hybrid_search(query, client, alpha, k)

        # print("Retrieved:", retrieved_ids)
        # print("Relevant:", relevant_ids)

        ndcg = compute_ndcg(retrieved_ids, relevant_ids, k)
        ndcg_scores.append(ndcg)
        # print(f"Alpha: {alpha}, NDCG@{k}: {ndcg:.4f}")

    total_score = sum(ndcg_scores)
    # print(f"Total Score: {total_score}")

    if total_score == 0:
        return 0.5

    weighted_alpha = sum(a * s for a, s in zip(alphas, ndcg_scores)) / total_score

    return weighted_alpha


queries_df = pd.read_csv(queries_path, encoding="utf-8", engine="python")

gt_df = pd.read_csv(ground_truth_path)

# Fix types
queries_df["query_id"] = queries_df["query_id"].astype(int)
gt_df["query_id"] = gt_df["query_id"].astype(int)

# Remove dummy row
queries_df = queries_df[queries_df["query_id"] != 1]

# Convert string list → actual list
gt_df["top_10_property_ids"] = gt_df["top_10_property_ids"].apply(ast.literal_eval)

# Create mappings
query_map = dict(zip(queries_df["query_id"], queries_df["query"]))
ground_truth_map = dict(zip(gt_df["query_id"], gt_df["top_10_property_ids"]))


with get_client() as client:
    for query_id, relevant_ids in ground_truth_map.items():
        try:
            user_query = query_map.get(query_id)

            if not user_query:
                print(f"⚠️ Query ID {query_id} not found in query file")
                continue

            print(f"\n🔎 Query ID: {query_id}")

            training_data_pipeline_test(query_id, user_query, client, relevant_ids)

        except Exception as e:
            print(f"Error processing Query ID {query_id}: {e}")

os.makedirs(os.path.dirname(output_path), exist_ok=True)

df = pd.DataFrame(results_log)
df["features"] = df["features"].apply(
    lambda x: json.dumps(x, ensure_ascii=False, default=str)
)

df.to_csv(output_path, index=False, encoding="utf-8")
