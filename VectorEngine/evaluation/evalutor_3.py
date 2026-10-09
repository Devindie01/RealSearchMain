import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
import json
import ast
import time
import traceback
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
from dotenv import load_dotenv

import sys
from pathlib import Path

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
from tests.dynamic_alpha import compute_alpha_from_entities
from app.query.formatter import create_weaviate_filter

# from app.query.executor.query_executor import QueryEmbedder


def _to_int(val):
    """Safely convert a property ID to int for consistent comparison."""
    try:
        return int(val)
    except (TypeError, ValueError):
        return val


def run_pipeline_test(user_query, client):
    print(f"\n{'='*60}\nQUERY: {user_query}")

    user_query = clean_query(user_query)

    res = extract_entities_from_user_query(user_query)
    entities = res["entities"]
    print(f"Extracted Entities: {entities}")

    # features = build_features(
    #     user_query, entities
    # )  # ✅ no fallback — real errors will surface
    # print(f"Extracted Features: {features}")

    type_label = queryclassifier(entities)

    classification = {"type": type_label}

    print(f"Type: {classification['type']}")

    if classification["type"] in ["Semantic", "Ambiguous"]:

        alpha = compute_alpha_from_entities(user_query, entities)
        print(f"Computed Alpha: {alpha}")

        properties = client.collections.get("Fyp_demo")

        results = properties.query.hybrid(
            query=user_query,
            # vector=query_vector,
            # filters=wv_filter,
            alpha=alpha,
            limit=100,
        )

        retrieved_ids = []
        if results.objects:
            for i, obj in enumerate(results.objects, 1):
                p = obj.properties
                pid = _to_int(p.get("propertyId"))
                retrieved_ids.append(pid)
                print(f" [{i}] {p.get('title')})")
        else:
            print(" No results found.")

        return retrieved_ids

    # elif classification["type"] == "Ambiguous":
    #     predicted_queries = expand_and_bound_ambiguous_query(user_query)
    #     print(f"Predicted Queries: {predicted_queries}")

    #     all_properties = []

    #     for i, pq in enumerate(predicted_queries, 1):
    #         properties = client.collections.get("RealSearchPropData")

    #         results = properties.query.hybrid(
    #             query=pq,  # ✅ IMPORTANT: use pq, not user_query
    #             alpha=1,
    #             limit=10,
    #         )

    #         if results.objects:
    #             all_properties.extend(results.objects)

    #     retrieved_ids = []
    #     seen = set()

    #     if all_properties:
    #         for i, obj in enumerate(all_properties, 1):
    #             p = obj.properties
    #             pid = _to_int(p.get("propertyId"))

    #             print(f" [{i}] {p.get('title')}")

    #             if pid is not None and pid not in seen:
    #                 seen.add(pid)
    #                 retrieved_ids.append(pid)

    #     # ✅ FINAL RETURN (this was missing)
    #     return retrieved_ids[:10] if retrieved_ids else []

    else:
        print("Non-semantic query detected. Skipping LLM extraction and vectorization.")


def compute_alpha(features):
    slot_coverage, slot_conf, non_slot_ratio, num_loc, num_prop = features

    # num_loc = min(num_loc / 3, 1.0)
    num_prop = min(num_prop / 3, 1.0)

    alpha = (
        +0.4 * non_slot_ratio
        # + 0.2 * num_loc
        + 0.2 * num_prop
        - 0.35 * slot_coverage
        - 0.35 * slot_conf
    )
    alpha = 0.5 + alpha
    alpha = max(0.1, min(0.9, alpha))

    return alpha


# ── Config ────────────────────────────────────────────────────────────────────
START_QUERY_ID = 2
END_QUERY_ID = 208

MAX_RETRIES = 3
RETRY_DELAY = 10
QUERY_DELAY = 1.0

failed_queries = []  # track queries that truly failed after all retries

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "final_ground_truth.csv")
per_query_out = os.path.join(current_dir, "per_query_results.json")
aggregated_out = os.path.join(current_dir, "results.json")
failed_out = os.path.join(current_dir, "failed_queries.json")

env_path = os.path.join(current_dir, "..", "app", ".env")
load_dotenv(dotenv_path=env_path)
print(f"✅ .env loaded from: {env_path}")


# ---------------------------------------------------------
# Load CSV data
# ---------------------------------------------------------
def load_data(csv_path, start_id, end_id):
    data = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query_id = row["query_id"]
            try:
                qid_int = int(query_id)
                if not (start_id <= qid_int <= end_id):
                    continue
            except ValueError:
                continue

            query_text = row["query"]
            try:
                relevant = ast.literal_eval(row["results"])
            except Exception:
                relevant = []

            data.append(
                {"query_id": query_id, "query": query_text, "relevant": relevant}
            )
    return data


# ---------------------------------------------------------
# Load existing results for resume
# ---------------------------------------------------------
def load_existing_results(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                results = json.load(f)
                done_ids = set(str(r["query_id"]) for r in results)
                print(f"♻️  Resuming — {len(done_ids)} queries already evaluated")
                return results, done_ids
            except Exception:
                pass
    print("🆕 Starting fresh")
    return [], set()


# ---------------------------------------------------------
# Save immediately
# ---------------------------------------------------------
def save_per_query(results, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)


def save_failed(failed, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(failed, f, indent=4)


# ---------------------------------------------------------
# Run pipeline with retry — NO hardcoded fallback
# ---------------------------------------------------------
def run_single_query(query_text, client):
    last_exception = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"    → Attempt {attempt}/{MAX_RETRIES}: running pipeline...")
            retrieved = run_pipeline_test(query_text, client)

            if isinstance(retrieved, dict):
                retrieved = retrieved.get("ids", [])
            if retrieved is None:
                raise ValueError("Pipeline returned None")

            print(f"    → Retrieved {len(retrieved)} results: {retrieved}")
            return retrieved

        except Exception as e:
            last_exception = e
            print(f"    ⚠️  Attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                print(f"    ⏳ Waiting {RETRY_DELAY}s before retry...")
                time.sleep(RETRY_DELAY)

    # All retries failed — raise so caller can log it properly
    raise last_exception


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
    print(f"\n{'='*60}")
    print(f"📂 CSV path    : {csv_path}")
    print(f"🔢 Query range : {START_QUERY_ID} → {END_QUERY_ID}")
    print(f"{'='*60}\n")

    data = load_data(csv_path, START_QUERY_ID, END_QUERY_ID)
    print(f"✅ Loaded {len(data)} queries in range [{START_QUERY_ID}, {END_QUERY_ID}]")

    per_query_results, done_ids = load_existing_results(per_query_out)
    queries_for_metrics = [
        {"retrieved": r.get("retrieved", []), "relevant": r.get("relevant", [])}
        for r in per_query_results
    ]

    total = len(data)
    print(f"\n🚀 Starting evaluation for {total} queries...\n{'='*60}")

    with get_client() as client:
        print("✅ Weaviate client connected\n")

        for i, item in enumerate(data, start=1):
            query_id = str(item["query_id"])
            query_text = item["query"]
            relevant = item["relevant"]

            if query_id in done_ids:
                print(f"⏭️  [{i}/{total}] Query ID {query_id} already done — skipping")
                continue

            print(f"\n{'='*60}")
            print(f"🔎 [{i}/{total}] Query ID : {query_id}")
            print(f"   Query     : {query_text[:120]}...")
            print(f"   Relevant  : {relevant}")

            try:
                retrieved = run_single_query(query_text, client)

                row = {
                    "query_id": query_id,
                    "retrieved": retrieved,
                    "relevant": relevant,
                    "precision@10": precision_at_k(retrieved, relevant),
                    "recall@10": recall_at_k(retrieved, relevant),
                    "f1@10": f1_at_k(retrieved, relevant),
                    "ndcg@10": ndcg_at_k(retrieved, relevant),
                }

                per_query_results.append(row)
                queries_for_metrics.append(
                    {"retrieved": retrieved, "relevant": relevant}
                )
                done_ids.add(query_id)

                save_per_query(per_query_results, per_query_out)
                print(
                    f"  💾 Saved — precision@10={row['precision@10']:.4f}  ndcg@10={row['ndcg@10']:.4f}"
                )
                print(f"✅ [{i}/{total}] Query ID {query_id} complete")

            except Exception as e:
                print(
                    f"❌ [{i}/{total}] Query ID {query_id} failed after all retries: {e}"
                )
                traceback.print_exc()
                failed_queries.append({"query_id": query_id, "error": str(e)})
                save_failed(failed_queries, failed_out)
                print(f"  📝 Logged to {failed_out}")

            time.sleep(QUERY_DELAY)

    print(f"\n{'='*60}")
    print(f"✅ Evaluation complete.")
    print(f"   Processed : {len(per_query_results)} queries")
    print(f"   Failed    : {len(failed_queries)} queries")

    final_results = evaluate(queries_for_metrics)

    with open(aggregated_out, "w") as f:
        json.dump(final_results, f, indent=4)

    with open(per_query_out, "w") as f:
        json.dump(per_query_results, f, indent=4)

    print(f"\n📊 Final Aggregated Metrics:")
    print(json.dumps(final_results, indent=4))
    print(f"\n💾 Saved to:")
    print(f"   {per_query_out}")
    print(f"   {aggregated_out}")
    if failed_queries:
        print(f"   {failed_out} ({len(failed_queries)} failed queries)")
