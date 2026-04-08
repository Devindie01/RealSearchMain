import os
import json
import csv
import time
import pandas as pd
from elasticsearch import Elasticsearch
print("🚀 Script started")
# ── Config ────────────────────────────────────────────────────────────────────
# For Elastic Cloud, use the Cloud ID from "Manage Deployment"
# and an API key created in Kibana / Stack Management.
CLOUD_ID        =  "53fd6bf97b434ff7a956bf16be7ac33d:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQzNmNiNTRkMGU0N2U0YzVkOTdlNzU1OTUzZTkwODM4ZCQzNmVmNWM2MDAwMTk0ZjNhYjg5ODFmMTk4NWJjODhiMQ=="
ELASTIC_API_KEY =  "ODZCUU5KMEJPM2llSl84V1hNVlg6V3VvaTRMODFvQUp4bHhEVm45aDVudw=="

# IMPORTANT:
# This must be the ACTUAL Elasticsearch index or alias, not just the Discover tab name
# unless your data view points exactly to an index/alias with the same name.
INDEX_NAME      = "realsearch"

# Use the exact field name that stores your property ID in Elasticsearch.
# Change this if your uploaded CSV created a different field name, e.g. "Property ID"
RETURN_FIELD    = "Property_id"

TOP_K           = 15
INPUT_FILE = "../queries/raw_queries.xlsx"
QUERY_DELAY     = 0.3
REQUEST_TIMEOUT = 60

# Adjust these to the exact field names in your index.
# Field names with spaces/capital letters are okay as long as they match exactly.
SEARCH_FIELDS = [
    "Description^3",
    "Full Description^2",
    "Location^2",
    "Nearest Town^2",
    "Amenities"
]

OUTPUT_JSON_CSV = "query_results_elasticsearch_top15.csv"
OUTPUT_FLAT_CSV = "query_results_elasticsearch_top15_flat.csv"

# ── Connect ───────────────────────────────────────────────────────────────────
client = Elasticsearch(
    cloud_id=CLOUD_ID,
    api_key=ELASTIC_API_KEY,
    request_timeout=REQUEST_TIMEOUT,
)

info = client.info()
print(f"Connected to cluster: {info['cluster_name']}")

# ── Optional: inspect one document to confirm field names ────────────────────
sample = client.search(
    index=INDEX_NAME,
    size=1,
    query={"match_all": {}},
    source=True,
)
if sample["hits"]["hits"]:
    print("Sample document fields:")
    print(list(sample["hits"]["hits"][0]["_source"].keys()))
else:
    raise RuntimeError(f"No documents found in index/alias '{INDEX_NAME}'")

# ── Load queries ──────────────────────────────────────────────────────────────
df = pd.read_excel(INPUT_FILE, header=None)
queries = df.iloc[:, 0].dropna().astype(str).tolist()
print(f"Loaded {len(queries)} queries from {INPUT_FILE}")

# ── Query Elasticsearch ───────────────────────────────────────────────────────
all_results = []
flat_rows = []

for query_text in queries:
    response = client.search(
        index=INDEX_NAME,
        size=TOP_K,
        source=[RETURN_FIELD],   # only return the property ID field
        query={
            "multi_match": {
                "query": query_text,
                "fields": SEARCH_FIELDS,
                "type": "best_fields"
            }
        }
    )

    results = []
    for rank, hit in enumerate(response["hits"]["hits"], start=1):
        prop_id = hit.get("_source", {}).get(RETURN_FIELD)

        # Fallback to Elasticsearch _id if the source field is missing
        if prop_id is None:
            prop_id = hit.get("_id", "")

        score = hit.get("_score", None)
        if score is not None:
            score = round(float(score), 4)

        row = {
            "propertyId": prop_id,
            "score": score,
            "rank": rank
        }
        results.append(row)

        flat_rows.append({
            "query": query_text,
            "rank": rank,
            "propertyId": prop_id,
            "score": score
        })

    all_results.append({
        "query": query_text,
        "results": results
    })

    print(f"  ✓ '{query_text}' → {len(results)} results")
    time.sleep(QUERY_DELAY)

# ── Save Weaviate-like CSV: query + JSON list ────────────────────────────────
with open(OUTPUT_JSON_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["query", "results_json"])
    for item in all_results:
        writer.writerow([item["query"], json.dumps(item["results"], ensure_ascii=False)])

print(f"Saved: {OUTPUT_JSON_CSV}")

# ── Save flat CSV: one row per result ────────────────────────────────────────
flat_df = pd.DataFrame(flat_rows)
flat_df.to_csv(OUTPUT_FLAT_CSV, index=False, encoding="utf-8")

print(f"Saved: {OUTPUT_FLAT_CSV}")

client.close()
print("Done!")