import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.query.executor.query_executor import QueryEmbedder
from app.query.query_expanision.classifer import JUNK_WORDS, queryclassifier
from traning_data_generation.feature_score_generation import build_features
from app.storage.connections import get_client
from app.query.query_expanision.query_normalizer import clean_query
from collections import defaultdict
import spacy
import pandas as pd
import json
import os
import numpy as np
import time
import traceback
import csv

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
merged_path  = os.path.join(BASE_DIR, "merged_dataset.csv")
output_path  = os.path.join(BASE_DIR, "traning_data_generation", "alpha_training_data.csv")

BATCH_SIZE        = 10
MAX_RETRIES       = 5      # retries per alpha
RETRY_DELAY       = 10     # seconds between retries
QUERY_DELAY       = 1.0    # seconds between queries
BATCH_DELAY       = 5      # seconds between batches
RECONNECT_RETRIES = 5      # how many times to try reconnecting
RECONNECT_DELAY   = 15     # seconds before reconnect attempt

# ── Load SpaCy model ──────────────────────────────────────────────────────────
nlp = spacy.load(os.path.join(BASE_DIR, "models", "model-best"))
print("✅ SpaCy model loaded successfully")

# ── Load merged dataset ───────────────────────────────────────────────────────
print(f"📂 Loading merged dataset from: {merged_path}")
merged_df = pd.read_csv(merged_path)
merged_df = merged_df[merged_df["query"].str.strip().str.lower() != "original"]
merged_df["results"] = merged_df["results"].apply(json.loads)
merged_df = merged_df.reset_index(drop=True)
print(f"✅ {len(merged_df)} rows ready to process")

# ── Setup output CSV ──────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(output_path), exist_ok=True)

if os.path.exists(output_path):
    existing_df = pd.read_csv(output_path)
    done_ids = set(existing_df["query_id"].astype(str).tolist())
    print(f"♻️  Resuming — {len(done_ids)} queries already done, skipping them")
else:
    done_ids = set()
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["query_id", "features", "alpha"])
    print("🆕 Starting fresh — output file created")


# ── Write single row immediately ──────────────────────────────────────────────
def write_row(query_id, features, alpha):
    with open(output_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            query_id,
            json.dumps(features, ensure_ascii=False, default=str),
            alpha
        ])


# ── Weaviate reconnect ────────────────────────────────────────────────────────
def get_weaviate_client():
    for attempt in range(1, RECONNECT_RETRIES + 1):
        try:
            print(f"  🔌 Connecting to Weaviate (attempt {attempt}/{RECONNECT_RETRIES})...")
            client = get_client().__enter__()
            print(f"  ✅ Weaviate connected")
            return client
        except Exception as e:
            print(f"  ⚠️ Connection attempt {attempt} failed: {e}")
            if attempt < RECONNECT_RETRIES:
                time.sleep(RECONNECT_DELAY)
            else:
                raise RuntimeError("❌ Could not connect to Weaviate after all retries")


# ── Helper functions ──────────────────────────────────────────────────────────

def entity_extraction(user_query):
    doc = nlp(user_query)
    raw_entities = defaultdict(list)

    for ent in doc.ents:
        words = ent.text.split()
        clean_text = " ".join(words[:-1]) if words[-1].lower() in JUNK_WORDS else ent.text
        raw_entities[ent.label_].append(clean_text)

    processed = {}
    for slot in ["property_type", "contract_type", "location", "no_of_bedrooms",
                 "no_of_bathrooms", "price", "land_size"]:
        if slot in raw_entities:
            processed[slot] = list(set(raw_entities[slot]))
    return processed


def compute_ndcg(retrieved_ids, relevant_ids, k=10):
    dcg = 0.0
    for i, doc_id in enumerate(retrieved_ids[:k]):
        if doc_id in relevant_ids:
            dcg += 1 / np.log2(i + 2)
    ideal_hits = min(len(relevant_ids), k)
    idcg = sum(1 / np.log2(i + 2) for i in range(ideal_hits))
    return 0.0 if idcg == 0 else dcg / idcg


def run_hybrid_search(user_query, client, alpha, k=10):
    print(f"    → Running hybrid search with alpha={alpha}...")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            classification = queryclassifier(user_query)
            embedder = QueryEmbedder()
            query_vector = embedder.get_vector(user_query)
            properties = client.collections.get("RealSearchPropData")
            results = properties.query.hybrid(
                query=user_query,
                vector=query_vector,
                alpha=alpha,
                limit=k,
            )
            retrieved_ids = []
            if getattr(results, "objects", None):
                for obj in results.objects:
                    retrieved_ids.append(obj.properties.get("propertyId"))
            print(f"    → alpha={alpha} retrieved {len(retrieved_ids)} results")
            return retrieved_ids, None   # success

        except Exception as e:
            print(f"    ⚠ Attempt {attempt}/{MAX_RETRIES} failed for alpha={alpha}: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                return [], e             # return the exception so caller can reconnect


def compute_best_alpha(query, client, relevant_ids, k=10):
    alphas = [0.0, 0.25, 0.5, 0.75, 1.0]
    ndcg_scores = []
    last_error = None

    for alpha in alphas:
        retrieved_ids, error = run_hybrid_search(query, client, alpha, k)
        if error is not None:
            last_error = error
        ndcg = compute_ndcg(retrieved_ids, relevant_ids, k)
        ndcg_scores.append(ndcg)
        print(f"    → alpha={alpha}  NDCG@{k}={ndcg:.4f}")

    total_score = sum(ndcg_scores)
    print(f"    Total NDCG: {total_score:.4f}")

    if total_score == 0:
        print(f"    ⚠️  Total score 0 — defaulting to 0.5")
        return 0.5, last_error

    weighted = sum(a * s for a, s in zip(alphas, ndcg_scores)) / total_score
    return weighted, last_error


def process_query(query_id, user_query, client, relevant_ids):
    user_query = clean_query(user_query)
    extraction = entity_extraction(user_query)
    print(f"  EXTRACTION: {extraction}")

    features = build_features(user_query, extraction)
    print(f"  FEATURES: {features}")

    relevant_ids_str = [str(x) for x in relevant_ids]
    best_alpha, last_error = compute_best_alpha(user_query, client, relevant_ids_str, k=10)
    print(f"  Best Alpha: {best_alpha}")

    write_row(query_id, features, best_alpha)
    print(f"  💾 Written to CSV")

    return last_error   # None if all good, exception if any alpha failed


# ── Main loop ─────────────────────────────────────────────────────────────────
total = len(merged_df)
print(f"\n🚀 Starting pipeline for {total} queries in batches of {BATCH_SIZE}...\n{'='*60}")

client = get_weaviate_client()

try:
    for batch_start in range(0, total, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, total)
        batch = merged_df.iloc[batch_start:batch_end]

        print(f"\n{'='*60}")
        print(f"📦 BATCH {batch_start // BATCH_SIZE + 1} — rows {batch_start + 1} to {batch_end} of {total}")
        print(f"{'='*60}")

        for i, row in enumerate(batch.itertuples(), start=batch_start + 1):
            query_id     = str(row.query_id)
            user_query   = row.query
            relevant_ids = row.results

            if query_id in done_ids:
                print(f"  ⏭️  [{i}/{total}] Query ID {query_id} already done — skipping")
                continue

            try:
                print(f"\n🔎 [{i}/{total}] Query ID: {query_id}")
                print(f"   Query: {str(user_query)[:120]}...")

                last_error = process_query(query_id, user_query, client, relevant_ids)
                done_ids.add(query_id)
                print(f"✅ [{i}/{total}] Query ID {query_id} complete")

                # If any alpha had an error, reconnect proactively before next query
                if last_error is not None:
                    print(f"  ⚠️  Some alphas had errors — reconnecting proactively...")
                    try:
                        client.close()
                    except Exception:
                        pass
                    time.sleep(RECONNECT_DELAY)
                    client = get_weaviate_client()

                time.sleep(QUERY_DELAY)

            except Exception as e:
                print(f"❌ [{i}/{total}] Error on Query ID {query_id}: {e}")
                traceback.print_exc()

                # Try to reconnect and continue
                print(f"  🔄 Attempting to reconnect to Weaviate...")
                try:
                    client.close()
                except Exception:
                    pass
                time.sleep(RECONNECT_DELAY)
                try:
                    client = get_weaviate_client()
                    print(f"  ✅ Reconnected — continuing from next query")
                except Exception as conn_err:
                    print(f"  ❌ Reconnect failed: {conn_err} — stopping")
                    raise

        print(f"\n📦 Batch done — sleeping {BATCH_DELAY}s before next batch...")
        time.sleep(BATCH_DELAY)

finally:
    try:
        client.close()
    except Exception:
        pass

print(f"\n{'='*60}")
print(f"🎉 All done! Results saved to {output_path}")