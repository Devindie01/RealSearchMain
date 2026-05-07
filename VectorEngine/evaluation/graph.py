"""
lambda_sweep_eval.py
--------------------
Sweeps lambda_ from 0.0 to 1.0 (step 0.1), re-runs the full evaluation
pipeline for each value, and plots all metrics against lambda.

Usage:
    python lambda_sweep_eval.py

Outputs:
    lambda_sweep_results.json   — raw per-lambda metric dict
    lambda_sweep_plot.png       — multi-metric line chart
"""

import sys
import os
import json
import time
import ast
import csv
import traceback

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from app.storage.connections import get_client
from tests.pipeline import run_pipeline_test
from evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    f1_at_k,
    ndcg_at_k,
    mean_reciprocal_rank,
    mean_average_precision,
)
from tests.dynamic_alpha import compute_alpha_from_entities

# ── Config ────────────────────────────────────────────────────────────────────
START_QUERY_ID = 2
END_QUERY_ID   = 185
MAX_RETRIES    = 3
RETRY_DELAY    = 10
QUERY_DELAY    = 0.5

LAMBDA_VALUES  = [round(x * 0.1, 1) for x in range(0, 11)]  # 0.0 … 1.0

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path    = os.path.join(current_dir, "evaluation", "final_ground_truth.csv")
results_out = os.path.join(current_dir, "lambda_sweep_results.json")
plot_out    = os.path.join(current_dir, "lambda_sweep_plot.png")
env_path    = os.path.join(current_dir, "app", ".env")

# Before (wrong — doubled up)
csv_path = os.path.join(current_dir, "evaluation", "final_ground_truth.csv")

# After (correct)
csv_path = os.path.join(current_dir, "final_ground_truth.csv")

load_dotenv(dotenv_path=env_path)
print(f"✅ .env loaded from: {env_path}")


# ── Data helpers ──────────────────────────────────────────────────────────────

def load_data(path, start_id, end_id):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                qid_int = int(row["query_id"])
            except ValueError:
                continue
            if not (start_id <= qid_int <= end_id):
                continue
            try:
                relevant = ast.literal_eval(row["results"])
            except Exception:
                relevant = []
            data.append({
                "query_id": row["query_id"],
                "query":    row["query"],
                "relevant": relevant,
            })
    return data


# ── Pipeline wrapper ──────────────────────────────────────────────────────────

def run_single_query(query_text, client, lambda_: float):
    """
    Passes lambda_ directly into run_pipeline_test, which forwards it to
    compute_alpha_from_entities(user_query, entities, lambda_=lambda_).
    """
    last_exc = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            retrieved = run_pipeline_test(query_text, client, lambda_)
            if isinstance(retrieved, dict):
                retrieved = retrieved.get("ids", [])
            if retrieved is None:
                raise ValueError("Pipeline returned None")
            return retrieved
        except Exception as e:
            last_exc = e
            print(f"    ⚠️  Attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
    raise last_exc


# ── Aggregation ───────────────────────────────────────────────────────────────

def aggregate(query_rows):
    if not query_rows:
        return {}
    p, r, f1, ndcg = [], [], [], []
    for q in query_rows:
        p.append(precision_at_k(q["retrieved"], q["relevant"]))
        r.append(recall_at_k(q["retrieved"],    q["relevant"]))
        f1.append(f1_at_k(q["retrieved"],       q["relevant"]))
        ndcg.append(ndcg_at_k(q["retrieved"],   q["relevant"]))
    return {
        "Precision@10": round(sum(p)    / len(p),    4),
        "Recall@10":    round(sum(r)    / len(r),    4),
        "F1@10":        round(sum(f1)   / len(f1),   4),
        "NDCG@10":      round(sum(ndcg) / len(ndcg), 4),
        "MRR":          round(mean_reciprocal_rank(query_rows),   4),
        "MAP":          round(mean_average_precision(query_rows), 4),
    }


# ── Plotting ──────────────────────────────────────────────────────────────────

METRIC_STYLES = {
    "Precision@10": {"color": "#2563eb", "marker": "o", "ls": "-"},
    "Recall@10":    {"color": "#16a34a", "marker": "s", "ls": "-"},
    "F1@10":        {"color": "#dc2626", "marker": "^", "ls": "-"},
    "NDCG@10":      {"color": "#9333ea", "marker": "D", "ls": "-"},
    "MRR":          {"color": "#ea580c", "marker": "P", "ls": "--"},
    "MAP":          {"color": "#0891b2", "marker": "X", "ls": "--"},
}

def plot_results(sweep: dict, out_path: str):
    lambdas = sorted(sweep.keys())
    metrics = [m for m in next(iter(sweep.values())).keys() if m != "failed_queries"]

    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#1e293b")

    for m in metrics:
        style = METRIC_STYLES.get(m, {"color": "white", "marker": "o", "ls": "-"})
        vals  = [sweep[lam][m] for lam in lambdas]
        ax.plot(
            lambdas, vals,
            color=style["color"], marker=style["marker"],
            linestyle=style["ls"], linewidth=2.0, markersize=7, label=m,
        )
        best_idx = int(np.argmax(vals))
        ax.annotate(
            f"{vals[best_idx]:.4f}",
            xy=(lambdas[best_idx], vals[best_idx]),
            xytext=(4, 6), textcoords="offset points",
            fontsize=7.5, color=style["color"],
        )

    ax.set_xlabel("lambda_", fontsize=13, color="#cbd5e1", labelpad=8)
    ax.set_ylabel("Score",   fontsize=13, color="#cbd5e1", labelpad=8)
    ax.set_title("Retrieval Metrics vs. Lambda", fontsize=16,
                 color="#f1f5f9", fontweight="bold", pad=14)
    ax.set_xticks(lambdas)
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))
    ax.tick_params(colors="#94a3b8")
    for spine in ax.spines.values():
        spine.set_edgecolor("#334155")
    ax.yaxis.grid(True, color="#334155", linewidth=0.6, linestyle="--")
    ax.set_axisbelow(True)
    ax.legend(loc="lower right", framealpha=0.25, labelcolor="#e2e8f0",
              fontsize=10, edgecolor="#475569")

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"📊 Plot saved → {out_path}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"📂 CSV          : {csv_path}")
    print(f"🔢 Query range  : {START_QUERY_ID} → {END_QUERY_ID}")
    print(f"🔁 Lambda values: {LAMBDA_VALUES}")
    print(f"{'='*60}\n")

    data = load_data(csv_path, START_QUERY_ID, END_QUERY_ID)
    print(f"✅ Loaded {len(data)} queries\n")

    if os.path.exists(results_out):
        with open(results_out) as f:
            sweep_results = json.load(f)
        print(f"♻️  Resuming — {len(sweep_results)} lambdas already done")
    else:
        sweep_results = {}

    with get_client() as client:
        print("✅ Weaviate client connected\n")

        for lam in LAMBDA_VALUES:
            lam_key = str(lam)

            if lam_key in sweep_results:
                print(f"⏭️  lambda={lam:.1f} already evaluated — skipping")
                continue

            print(f"\n{'='*60}")
            print(f"🔬 Evaluating lambda = {lam:.1f}")
            print(f"{'='*60}")

            query_rows   = []
            failed_count = 0

            for idx, item in enumerate(data, start=1):
                qid        = item["query_id"]
                query_text = item["query"]
                relevant   = item["relevant"]

                print(f"  [{idx}/{len(data)}] QID={qid} | {query_text[:80]}...")

                try:
                    retrieved = run_single_query(query_text, client, lam)
                    query_rows.append({"retrieved": retrieved, "relevant": relevant})
                    print(f"    ✅ {len(retrieved)} results retrieved")
                except Exception as e:
                    print(f"    ❌ QID={qid} failed: {e}")
                    traceback.print_exc()
                    failed_count += 1

                time.sleep(QUERY_DELAY)

            metrics = aggregate(query_rows)
            metrics["failed_queries"] = failed_count
            sweep_results[lam_key] = metrics

            print(f"\n  📈 lambda={lam:.1f} → {metrics}")

            with open(results_out, "w") as f:
                json.dump(sweep_results, f, indent=4)
            print(f"  💾 Saved → {results_out}")

    numeric_sweep = {float(k): v for k, v in sweep_results.items()}
    plot_results(numeric_sweep, plot_out)

    print(f"\n{'='*60}")
    print(f"✅ Lambda sweep complete!")
    print(f"   Results : {results_out}")
    print(f"   Plot    : {plot_out}")
    print(f"{'='*60}\n")

    print(f"{'Lambda':<10} {'P@10':<10} {'R@10':<10} {'F1@10':<10} "
          f"{'NDCG@10':<10} {'MRR':<10} {'MAP':<10}")
    print("-" * 70)
    for lam in LAMBDA_VALUES:
        m = sweep_results.get(str(lam), {})
        if not m:
            continue
        print(
            f"{lam:<10.1f} "
            f"{m.get('Precision@10', 0):<10.4f} "
            f"{m.get('Recall@10',    0):<10.4f} "
            f"{m.get('F1@10',        0):<10.4f} "
            f"{m.get('NDCG@10',      0):<10.4f} "
            f"{m.get('MRR',          0):<10.4f} "
            f"{m.get('MAP',          0):<10.4f}"
        )