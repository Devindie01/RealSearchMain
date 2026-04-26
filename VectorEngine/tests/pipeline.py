import sys
from pathlib import Path

# Ensure the project root (VectorEngine) is on sys.path so the `app` package
# can be imported when running this test directly (e.g. `python tests/...`).
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from traning_data_generation.feature_score_generation import build_features
from app.query.query_expanision.query_normalizer import clean_query
from app.query.query_expanision.post_processing import build_query_segments
from app.query.query_expanision.classifer import (
    extract_entities_from_user_query,
    queryclassifier,
)
from app.query.query_expanision.semantic_query_handler import get_alpha_from_entities
from app.query.query_expanision.ambiguous_query_handler import (
    expand_and_bound_ambiguous_query,
)
from app.query.formatter import create_weaviate_filter
from app.query.executor.query_executor import QueryEmbedder


def run_pipeline_test(user_query, client):
    print(f"\n{'='*60}\nQUERY: {user_query}")

    user_query = clean_query(user_query)

    # Step A: NLP Classification

    # --- Find this section in run_pipeline_test ---

    res = extract_entities_from_user_query(user_query)
    entities = res["entities"]
    print(f"Extracted Entities: {entities}")
    
    features = build_features(user_query, entities)
    print(f"Extracted Features: {features}")
    
    alpha = compute_alpha(features)
    print(f"Computed Alpha: {alpha}")
    
    type_label = queryclassifier(features)
    classification = {"type": type_label} 

    print(f"Type: {classification['type']} | Alpha: {alpha:.3f}")

    if classification["type"] == "Semantic":

        result_segment = build_query_segments(user_query, entities)

        print (f"Query Segment: {result_segment}")

        # Step C: Vectorization
        embedder = QueryEmbedder()
        query_vector = embedder.get_vector(user_query)

        # Step D: Filter Construction
        wv_filter = create_weaviate_filter(result_segment)

        # Step E: Weaviate Hybrid Search
        properties = client.collections.get("RealSearchPropData")

        results = properties.query.hybrid(
            query=user_query,  # Keyword part
            vector=query_vector,  # Vector part
            # filters=wv_filter,  # Hard metadata filters
            alpha=alpha,  # Dynamically calculated weight
            limit=10,
        )
        # Print Results
        if results.objects:
            for i, obj in enumerate(results.objects, 1):
                p = obj.properties
                print(f" [{i}] {p.get('title')})")
        else:
            print(" No results found.")

    elif classification["type"] == "Ambiguous":
        predicted_queries = expand_and_bound_ambiguous_query(user_query)
        print(f"Predicted Queries: {predicted_queries}")
        all_properties = []
        for i, pq in enumerate(predicted_queries, 1):
            embedder = QueryEmbedder()
            query_vector = embedder.get_vector(pq)
            properties = client.collections.get("RealSearchPropData")

            results = properties.query.hybrid(
                query=user_query,  # Keyword part
                vector=query_vector,  # Vector part
                alpha=1,  # Dynamically calculated weight
                limit=10,
            )
            all_properties.append(results.objects)

        if all_properties:
            for i, obj_list in enumerate(all_properties, 1):
                for j, obj in enumerate(obj_list, 1):
                    p = obj.properties
                    print(f" [{i}.{j}] {p.get('title')}")

    else:
        print("Non-semantic query detected. Skipping LLM extraction and vectorization.")



def compute_alpha(features):
    slot_coverage, slot_conf, non_slot_ratio, num_loc, num_prop = features

    # normalize counts
    num_loc = min(num_loc / 3, 1.0)
    num_prop = min(num_prop / 3, 1.0)

    # weighted combination
    alpha = (
        + 0.4 * non_slot_ratio         # more natural language → semantic
        + 0.2 * num_loc                # ambiguity → semantic
        + 0.1 * num_prop               # ambiguity → semantic
        - 0.3 * slot_coverage          # structured → keyword
        - 0.3 * slot_conf              # reliable structure → keyword
    )

    # shift to center around 0.5
    alpha = 0.5 + alpha

    # clamp
    alpha = max(0.1, min(0.9, alpha))

    return alpha
