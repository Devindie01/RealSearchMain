import csv
import json
import ast
from evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    f1_at_k,
    ndcg_at_k,
    mean_reciprocal_rank,
    mean_average_precision,
)
from app.storage.connections import get_client
from tests.pipeline import run_pipeline_test

import os
from dotenv import load_dotenv

# Load the .env file located in the app directory
# We use an absolute path or join it based on the file location to be safe
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, "..", "app", ".env")
load_dotenv(dotenv_path=env_path)


# ---------------------------------------------------------
# Load CSV data
# ---------------------------------------------------------
def load_data(csv_path):
    data = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            query_id = row["query_id"]
            query_text = row["query"]

            # Convert string "[1, 2, 3]" → list
            try:
                # Use literal_eval for safety over eval()
                relevant = ast.literal_eval(row["results"])
            except Exception:
                relevant = []

            data.append(
                {"query_id": query_id, "query": query_text, "relevant": relevant}
            )

    return data


# ---------------------------------------------------------
# Run pipeline + collect metrics input
# ---------------------------------------------------------
def run_evaluation(data, client):
    queries_for_metrics = []
    per_query_results = []

    for item in data:
        query_id = item["query_id"]
        query_text = item["query"]
        relevant = item["relevant"]

        print(f"Processing query {query_id}...")

        try:
            # Run your retrieval system
            retrieved = run_pipeline_test(query_text, client)

            # If pipeline returns dict like {"ids": [...]}
            if isinstance(retrieved, dict):
                retrieved = retrieved.get("ids", [])

            if retrieved is None:
                retrieved = []

            queries_for_metrics.append({"retrieved": retrieved, "relevant": relevant})

            per_query_results.append(
                {
                    "query_id": query_id,
                    "precision@10": precision_at_k(retrieved, relevant),
                    "recall@10": recall_at_k(retrieved, relevant),
                    "f1@10": f1_at_k(retrieved, relevant),
                    "ndcg@10": ndcg_at_k(retrieved, relevant),
                }
            )

        except Exception as e:
            print(f"Error processing query {query_id}: {e}")

    return queries_for_metrics, per_query_results


# ---------------------------------------------------------
# Aggregate metrics
# ---------------------------------------------------------
def evaluate(queries):
    if not queries:
        return {}

    p, r, f1, ndcg = [], [], [], []

    for q in queries:
        retrieved = q["retrieved"]
        relevant = q["relevant"]

        p.append(precision_at_k(retrieved, relevant))
        r.append(recall_at_k(retrieved, relevant))
        f1.append(f1_at_k(retrieved, relevant))
        ndcg.append(ndcg_at_k(retrieved, relevant))

    return {
        "Precision@10": sum(p) / len(p),
        "Recall@10": sum(r) / len(r),
        "F1@10": sum(f1) / len(f1),
        "NDCG@10": sum(ndcg) / len(ndcg),
        "MRR": mean_reciprocal_rank(queries),
        "MAP": mean_average_precision(queries),
    }


# ---------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":
    # Update this path to your local file location
    csv_path = r"D:\FYP\RealSearch\VectorEngine\evaluation\final_ground_truth.csv"

    # 1. Load dataset
    data = load_data(csv_path)

    # 2. Run evaluation
    with get_client() as client:
        queries, per_query = run_evaluation(data, client)

    # 3. Compute final aggregated metrics
    final_results = evaluate(queries)

    # 4. Save outputs to JSON files
    with open("results.json", "w") as f:
        json.dump(final_results, f, indent=4)

    with open("per_query_results.json", "w") as f:
        json.dump(per_query, f, indent=4)

    print("\nEvaluation completed successfully.")
    print("Final Aggregated Metrics:")
    print(json.dumps(final_results, indent=4))
