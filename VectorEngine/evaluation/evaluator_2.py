import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
import json
import ast
import glob
from evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    f1_at_k,
    ndcg_at_k,
    mean_reciprocal_rank,
    mean_average_precision,
)

# ── Config ────────────────────────────────────────────────────────────────────
current_dir       = os.path.dirname(os.path.abspath(__file__))
ground_truth_dir  = os.path.join(current_dir, "ground_truth_207")
weaviate_dir      = os.path.join(current_dir, "weaviate_results")
output_file       = os.path.join(current_dir, "baseline_evaluation_results.json")

BASELINE_FILES = {
    "alpha_0"  : os.path.join(weaviate_dir, "query_results_alpha_0.csv"),
    "alpha_0.5": os.path.join(weaviate_dir, "query_results_alpha_0.5.csv"),
    "alpha_1"  : os.path.join(weaviate_dir, "query_results_alpha_1.csv"),
}


# ── Load all ground truth files ───────────────────────────────────────────────
def load_ground_truth(gt_dir):
    gt_files = sorted(glob.glob(os.path.join(gt_dir, "ground_truth_*.csv")))
    print(f"📂 Found {len(gt_files)} ground truth files")

    gt_lookup = {}
    for f in gt_files:
        with open(f, "r", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                try:
                    qid = int(row["query_id"])
                    relevant = ast.literal_eval(row["top_10_property_ids"])
                    gt_lookup[qid] = relevant
                except Exception as e:
                    print(f"  ⚠️ Skipping row in {os.path.basename(f)}: {e}")

    print(f"✅ Ground truth loaded: {len(gt_lookup)} queries\n")
    return gt_lookup


# ── Load a baseline results CSV ───────────────────────────────────────────────
def load_baseline(csv_path):
    results = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = row["query"]
            if query.strip().lower() == "original":
                continue
            try:
                items = json.loads(row["results_json"])
                property_ids = [item["propertyId"] for item in items]
                results[query] = property_ids
            except Exception as e:
                print(f"  ⚠️ Skipping row for query '{query[:50]}': {e}")
    return results


# ── Load raw queries to map query_id → query text ────────────────────────────
def load_raw_queries(csv_path):
    query_map = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                qid = int(row["query_id"])
                query_map[qid] = row["query"]
            except Exception:
                continue
    return query_map


# ── Aggregate metrics ─────────────────────────────────────────────────────────
def evaluate(queries_for_metrics):
    if not queries_for_metrics:
        return {}

    p, r, f1, ndcg = [], [], [], []
    for q in queries_for_metrics:
        retrieved = q["retrieved"]
        relevant  = q["relevant"]
        p.append(precision_at_k(retrieved, relevant))
        r.append(recall_at_k(retrieved, relevant))
        f1.append(f1_at_k(retrieved, relevant))
        ndcg.append(ndcg_at_k(retrieved, relevant))

    return {
        "Precision@10": round(sum(p)    / len(p),    4),
        "Recall@10"   : round(sum(r)    / len(r),    4),
        "F1@10"       : round(sum(f1)   / len(f1),   4),
        "NDCG@10"     : round(sum(ndcg) / len(ndcg), 4),
        "MRR"         : round(mean_reciprocal_rank(queries_for_metrics),   4),
        "MAP"         : round(mean_average_precision(queries_for_metrics), 4),
        "num_queries" : len(queries_for_metrics),
    }


# ── Evaluate one baseline against ground truth ────────────────────────────────
def evaluate_baseline(name, baseline_csv, gt_lookup, query_map):
    print(f"\n{'='*60}")
    print(f"📊 Evaluating baseline: {name}")
    print(f"   File: {baseline_csv}")
    print(f"{'='*60}")

    baseline_results = load_baseline(baseline_csv)
    print(f"✅ Loaded {len(baseline_results)} queries from baseline CSV\n")

    # Build reverse map: query_text → query_id
    text_to_id = {v: k for k, v in query_map.items()}

    queries_for_metrics = []
    per_query = []
    skipped = 0

    for query_text, retrieved_ids in baseline_results.items():
        query_id = text_to_id.get(query_text)

        # 🔒 FILTER: only evaluate queries 2–185
        if query_id is None or not (2 <= query_id <= 185):
            skipped += 1
            continue

        relevant = gt_lookup.get(query_id, [])
        if not relevant:
            skipped += 1
            continue

        # Ensure type consistency — both as int
        retrieved_int = []
        for pid in retrieved_ids:
            try:
                retrieved_int.append(int(pid))
            except Exception:
                retrieved_int.append(pid)

        relevant_int = []
        for pid in relevant:
            try:
                relevant_int.append(int(pid))
            except Exception:
                relevant_int.append(pid)

        p   = round(precision_at_k(retrieved_int, relevant_int), 4)
        r   = round(recall_at_k(retrieved_int, relevant_int),    4)
        f1  = round(f1_at_k(retrieved_int, relevant_int),        4)
        ndcg= round(ndcg_at_k(retrieved_int, relevant_int),      4)

        # ✅ Print per-query details
        print(f"  Query ID  : {query_id}")
        print(f"  Query     : {query_text[:100]}...")
        print(f"  Retrieved : {retrieved_int}")
        print(f"  Relevant  : {relevant_int}")
        print(f"  P@10={p}  R@10={r}  F1@10={f1}  NDCG@10={ndcg}")
        print()

        queries_for_metrics.append({
            "retrieved": retrieved_int,
            "relevant" : relevant_int,
        })

        per_query.append({
            "query_id"     : query_id,
            "query"        : query_text[:80],
            "retrieved"    : retrieved_int,
            "relevant"     : relevant_int,
            "precision@10" : p,
            "recall@10"    : r,
            "f1@10"        : f1,
            "ndcg@10"      : ndcg,
        })

    print(f"{'='*60}")
    print(f"   Matched  : {len(queries_for_metrics)} queries")
    print(f"   Skipped  : {skipped} (no match in ground truth or query map)")

    aggregated = evaluate(queries_for_metrics)

    print(f"\n   Aggregated results for {name}:")
    for k, v in aggregated.items():
        print(f"     {k}: {v}")

    return aggregated, per_query


# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"🚀 Baseline Evaluation")
    print(f"{'='*60}")

    # Load ground truth
    gt_lookup = load_ground_truth(ground_truth_dir)

    # Load raw queries (to map query text → query_id)
    raw_queries_path = os.path.join(current_dir, "raw_queries.csv")
    query_map = load_raw_queries(raw_queries_path)
    print(f"✅ Query map loaded: {len(query_map)} queries")

    # Evaluate each baseline
    all_results   = {}
    all_per_query = {}

    for name, csv_path in BASELINE_FILES.items():
        if not os.path.exists(csv_path):
            print(f"\n⚠️  File not found, skipping: {csv_path}")
            continue

        aggregated, per_query = evaluate_baseline(name, csv_path, gt_lookup, query_map)
        all_results[name]   = aggregated
        all_per_query[name] = per_query

    # ── Print comparison table ─────────────────────────────────────────────────
    print(f"\n\n{'='*60}")
    print(f"📊 COMPARISON TABLE")
    print(f"{'='*60}")
    metrics = ["Precision@10", "Recall@10", "F1@10", "NDCG@10", "MRR", "MAP"]
    header = f"{'Metric':<15}" + "".join(f"{name:<15}" for name in all_results)
    print(header)
    print("-" * len(header))
    for metric in metrics:
        row = f"{metric:<15}"
        for name in all_results:
            val = all_results[name].get(metric, "N/A")
            row += f"{str(val):<15}"
        print(row)

    # ── Save outputs ───────────────────────────────────────────────────────────
    final_output = {
        "aggregated": all_results,
        "per_query" : all_per_query,
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4)

    print(f"\n💾 Results saved to: {output_file}")