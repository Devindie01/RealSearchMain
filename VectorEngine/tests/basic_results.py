import pandas as pd
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.storage.connections import get_client
from tests.pipeline import run_pipeline_test

from app.query.query_expanision.classifer import (
    queryclassifier,
    map_entities_to_query_segment,
)
from app.query.query_expanision.semantic_query_handler import get_alpha_from_srr
from app.query.query_expanision.ambiguous_query_handler import (
    expand_and_bound_ambiguous_query,
)
from app.query.formatter import create_weaviate_filter
from app.query.executor.query_executor import QueryEmbedder, get_chain

# Initialize the chain
chain = get_chain()


def process_queries_to_file(csv_path, output_path):
    # 1. Load the CSV
    # Ensure the column name matches your CSV header (e.g., 'Semantic')
    df = pd.read_csv(csv_path)
    queries = df["Original"].tolist()

    results_map = {}

    with get_client() as client:
        for q in queries[0:10]:
            if pd.isna(q):
                continue  # Skip empty rows

            try:
                # 2. Run your pipeline
                # Assuming run_pipeline_test returns a list of property objects/dicts
                retrieved_properties = basic_run_pipeline_test(q, client)

                # 3. Store in dictionary
                results_map[q] = retrieved_properties

            except Exception as e:
                print(f"Error processing '{q}': {e}")

                results_map[q] = f"Error: {str(e)}"

    # 4. Save to a JSON file (Key-Value format)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results_map, f, indent=4, ensure_ascii=False)

    print(f"\nDone! Results saved to {output_path}")


def basic_run_pipeline_test(user_query, client):
    print(f"\n{'='*60}\nQUERY: {user_query}")

    # Step A: NLP Classification
    classification = queryclassifier(user_query)
    alpha = get_alpha_from_srr(classification)

    print(
        f"Type: {classification['type']} | SRR: {classification['SRR']:.2f} | Alpha: {alpha}"
    )

    if classification["type"] == "Semantic":

        entities = classification["entities"]
        leftover = classification["leftover_text"]

        result_segment = map_entities_to_query_segment(user_query, entities, leftover)

        # Step C: Vectorization
        embedder = QueryEmbedder()
        query_vector = embedder.get_vector(user_query)

        # Step D: Filter Construction
        wv_filter = create_weaviate_filter(result_segment)

        # Step E: Weaviate Hybrid Search
        properties = client.collections.get("RealSearchPropData1")

        results = properties.query.hybrid(
            query=user_query,  # Keyword part
            vector=query_vector,  # Vector part
            filters=wv_filter,  # Hard metadata filters
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
            properties = client.collections.get("RealSearchPropData1")

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


# Configuration
csv_file_path = (
    r"D:\FYP\RealSearch\VectorEngine\query_data\RealSearch Leads - Queries.csv"
)
output_file_path = "basic_retrieved_results.json"

# Execute
process_queries_to_file(csv_file_path, output_file_path)
