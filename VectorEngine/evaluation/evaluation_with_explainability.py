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
from explainability.explainability import ExplainabilityEngine
from dotenv import load_dotenv

# ── Config ────────────────────────────────────────────────────────────────────
START_QUERY_ID = 2
END_QUERY_ID = 208
MAX_RETRIES = 3
RETRY_DELAY = 10
QUERY_DELAY = 1.0

failed_queries = []

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "final_ground_truth.csv")
per_query_out = os.path.join(current_dir, "per_query_results.json")
aggregated_out = os.path.join(current_dir, "results.json")
failed_out = os.path.join(current_dir, "failed_queries.json")
explanations_csv_out = os.path.join(current_dir, "explanations_results.csv")  # ← new
env_path = os.path.join(current_dir, "..", "app", ".env")

load_dotenv(dotenv_path=env_path)
print(f"✅ .env loaded from: {env_path}")

# ── Explainability engine (singleton — one LLM client for the whole run) ──────
explainer = ExplainabilityEngine()


# ---------------------------------------------------------
# Fetch property description from Weaviate by property_id
# ---------------------------------------------------------
def fetch_property_description(client, property_id) -> str:
    try:
        from weaviate.classes.query import Filter

        collection = client.collections.get("RealSearchPropData1")
        result = collection.query.fetch_objects(
            filters=Filter.by_property("propertyId").equal(str(property_id)),
            return_properties=["description"],
            limit=1,
        )
        if result.objects:
            return result.objects[0].properties.get("description", "")
    except Exception as e:
        print(f"    ⚠️  Could not fetch description for {property_id}: {e}")
    return ""


# ---------------------------------------------------------
# Generate explanations for the top-K retrieved properties
# ---------------------------------------------------------
def generate_explanations(
    client,
    query_text: str,
    retrieved_ids: list,
    top_k: int = 10,
) -> list[dict]:
    """
    Call ExplainabilityEngine for the first `top_k` retrieved properties.

    Returns a list of explanation dicts:
        [{"property_id": ..., "explanation": ...}, ...]
    """
    explanations = []
    for prop_id in retrieved_ids[:top_k]:
        description = fetch_property_description(client, prop_id)
        if not description:
            print(f"    ⚠️  No description found for {prop_id} — skipping explanation")
            continue
        try:
            result = explainer.explain(
                user_query=query_text,
                property_id=prop_id,
                property_description=description,
            )
            explanations.append(
                {
                    "property_id": result["property_id"],
                    "description": description,          # ← new
                    "explanation": result["explanation"],
                }
            )
            print(f"    💬 Explained {prop_id}: {result['explanation']}")
        except Exception as e:
            print(f"    ⚠️  Explanation failed for {prop_id}: {e}")
            explanations.append(
                {
                    "property_id": prop_id,
                    "description": description,          # ← still capture description even if explanation fails
                    "explanation": "",
                }
            )
    return explanations


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
# Save explanations CSV
# Each row = one retrieved property for a given query.
# Columns: query_id, query, rank, property_id, explanation
# ---------------------------------------------------------
CSV_FIELDNAMES = ["query_id", "query", "rank", "property_id", "property_description", "explanation"]


def init_csv(output_path: str) -> None:
    """Write the CSV header if the file does not already exist (resume-safe)."""
    if not os.path.exists(output_path):
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()
        print(f"📄 CSV initialised → {output_path}")


def append_query_to_csv(result: dict, output_path: str) -> None:
    """
    Append all retrieved-property rows for a single query to the CSV.
    Called immediately after each query completes so progress is never lost.

    Columns
    -------
    query_id             : identifier of the query
    query                : full query text
    rank                 : 1-based position in the retrieved list
    property_id          : the retrieved property's ID
    property_description : Weaviate property description (empty if not available)
    explanation          : LLM-generated explanation (empty if not available)
    """
    query_id   = result.get("query_id", "")
    query_text = result.get("query", "")
    retrieved  = result.get("retrieved", [])

    # Build a lookup from property_id → {description, explanation}
    exp_map = {
        exp["property_id"]: {
            "property_description": exp.get("description", ""),
            "explanation": exp.get("explanation", ""),
        }
        for exp in result.get("explanations", [])
    }

    with open(output_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        for rank, prop_id in enumerate(retrieved, start=1):
            meta = exp_map.get(prop_id, {})
            writer.writerow(
                {
                    "query_id":             query_id,
                    "query":                query_text,
                    "rank":                 rank,
                    "property_id":          prop_id,
                    "property_description": meta.get("property_description", ""),
                    "explanation":          meta.get("explanation", ""),
                }
            )


# ---------------------------------------------------------
# Run pipeline with retry
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

        init_csv(explanations_csv_out)

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
                # ── 1. Retrieve property IDs ───────────────────────────────
                retrieved = run_single_query(query_text, client)

                # ── 2. Generate explanations for top-10 results ────────────
                print(f"   💬 Generating explanations for top-10 results...")
                explanations = generate_explanations(
                    client=client,
                    query_text=query_text,
                    retrieved_ids=retrieved,
                    top_k=10,
                )

                # ── 3. Build result row (metrics + explanations) ───────────
                row = {
                    "query_id": query_id,
                    "query": query_text,
                    "retrieved": retrieved,
                    "relevant": relevant,
                    "precision@10": precision_at_k(retrieved, relevant),
                    "recall@10": recall_at_k(retrieved, relevant),
                    "f1@10": f1_at_k(retrieved, relevant),
                    "ndcg@10": ndcg_at_k(retrieved, relevant),
                    "explanations": explanations,
                }

                per_query_results.append(row)
                queries_for_metrics.append(
                    {"retrieved": retrieved, "relevant": relevant}
                )
                done_ids.add(query_id)
                save_per_query(per_query_results, per_query_out)
                append_query_to_csv(row, explanations_csv_out)

                print(
                    f"  💾 Saved — precision@10={row['precision@10']:.4f}  "
                    f"ndcg@10={row['ndcg@10']:.4f}  "
                    f"explanations={len(explanations)}"
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
    print(f"   {explanations_csv_out}")
    if failed_queries:
        print(f"   {failed_out} ({len(failed_queries)} failed queries)")