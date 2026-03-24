


WEAVIATE_URL = "https://bzt3mqsssyqvga8h73qua.c0.asia-southeast1.gcp.weaviate.cloud"
WEAVIATE_API_KEY = "bjRYdFh3TElZazgrWFFNY19ib01iU2NsVHdEWCtjQlRxeS95Z3RtdUlIVVZqZXo2M1dVMUxGaWxhT3JBPV92MjAw"

import os
import json
import csv
import pandas as pd
import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.query import MetadataQuery
from weaviate.classes.init import Auth, AdditionalConfig, Timeout

import time

# ── Config ────────────────────────────────────────────────────────────────────


COLLECTION_NAME  = "RealSearchPropNew"          # ← change to your collection name
RETURN_FIELDS    = ["propertyId"]      # ← fields to return from each result
TOP_K            = 15                 # ← number of results per query

ALPHA_VALUES     = [1.0, 0.5, 0.0]     # ← add/change alpha values here

INPUT_FILE       = "raw_queries.xlsx"  # ← your input file
QUERY_DELAY      = 0.5

# ── Connect ───────────────────────────────────────────────────────────────────

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=60)  # increased timeouts
    ),
)

print(f"Weaviate ready: {client.is_ready()}")


# ── Load queries ──────────────────────────────────────────────────────────────

df = pd.read_excel(INPUT_FILE, header=None)
queries = df.iloc[:, 0].dropna().astype(str).tolist()
print(f"Loaded {len(queries)} queries from {INPUT_FILE}")


# ── Query Weaviate for each alpha ─────────────────────────────────────────────

collection = client.collections.get(COLLECTION_NAME)

for alpha in ALPHA_VALUES:
    print(f"\nRunning queries with alpha={alpha} ...")
    all_results = []

    for query_text in queries:
        if alpha == 1.0:
            # Pure vector search — returns certainty
            response = collection.query.near_text(
                query=query_text,
                limit=TOP_K,
                return_metadata=MetadataQuery(certainty=True),
            )
            results = []
            for obj in response.objects:
                results.append({
                    "propertyId": obj.properties.get("propertyId", ""),
                    "certainty": round(obj.metadata.certainty, 4) if obj.metadata.certainty is not None else None,
                })
        else:
            # Hybrid search — returns score
            response = collection.query.hybrid(
                query=query_text,
                alpha=alpha,
                limit=TOP_K,
                return_metadata=MetadataQuery(score=True),
            )
            results = []
            for obj in response.objects:
                results.append({
                    "propertyId": obj.properties.get("propertyId", ""),
                    "score": round(obj.metadata.score, 4) if obj.metadata.score is not None else None,
                })

        all_results.append({
            "query": query_text,
            "results": results,
        })

        print(f"  ✓ '{query_text}' → {len(results)} results")
        time.sleep(QUERY_DELAY)  # small delay to avoid overwhelming the server

    # Format alpha for filename: 1.0 → "1", 0.0 → "0", 0.5 → "0.5"
    alpha_str = str(alpha).rstrip("0").rstrip(".")
    output_file = f"query_results_alpha_{alpha_str}.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["query", "results_json"])
        for item in all_results:
            writer.writerow([item["query"], json.dumps(item["results"])])

    print(f"  → Saved to {output_file}")


client.close()
print("\nDone!")