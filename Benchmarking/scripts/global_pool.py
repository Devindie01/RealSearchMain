import pandas as pd
import json
from pathlib import Path

# ----------------------------
# File paths
# ----------------------------
BASE_DIR = Path("../outputs")

file_map = {
    "alpha_0": "../outputs/weaviate_results/query_results_alpha_0.csv",
    "alpha_0.5": "../outputs/weaviate_results/query_results_alpha_0.5.csv",
    "alpha_1": "../outputs/weaviate_results/query_results_alpha_1.csv",
    "elastic": "../outputs/elasticSearch_results/query_results_elasticsearch_top15.csv",
}

# ----------------------------
# Helpers
# ----------------------------
def parse_results(results_json_str):
    try:
        return json.loads(results_json_str)
    except Exception as e:
        print("Error parsing JSON:", e)
        return []

def get_ids_simple(results):
    return [item["propertyId"] for item in results]

def get_ids_elastic(results):
    results_sorted = sorted(results, key=lambda x: x.get("rank", 999))
    return [item["propertyId"] for item in results_sorted]

# ----------------------------
# Load CSVs
# ----------------------------
dfs = {key: pd.read_csv(path) for key, path in file_map.items()}

# ----------------------------
# Limit to 207 queries
# ----------------------------
NUM_QUERIES = 207
queries_list = dfs["alpha_0"]["query"].tolist()[:NUM_QUERIES]

# ----------------------------
# Create query_id mapping
# ----------------------------
query_rows = []
query_id_map = {}

for idx, query in enumerate(queries_list, start=1):
    query_id_map[idx] = query
    query_rows.append({
        "query_id": idx,
        "query": query
    })

# ----------------------------
# Output containers
# ----------------------------
non_dedup_rows = []
dedup_rows = []

# ----------------------------
# Main loop
# ----------------------------
for i in range(NUM_QUERIES):
    query_id = i + 1

    all_ids_ordered = []

    # 1. Elasticsearch (ranked)
    elastic_results = parse_results(dfs["elastic"].iloc[i]["results_json"])
    all_ids_ordered.extend(get_ids_elastic(elastic_results))

    # 2. Weaviate (priority order)
    for key in ["alpha_1", "alpha_0.5", "alpha_0"]:
        results = parse_results(dfs[key].iloc[i]["results_json"])
        all_ids_ordered.extend(get_ids_simple(results))

    # Non-deduplicated
    non_dedup_rows.append({
        "query_id": query_id,
        "property_ids": all_ids_ordered
    })

    # Deduplicated (preserve order)
    seen = set()
    dedup_ids = []
    for pid in all_ids_ordered:
        if pid not in seen:
            seen.add(pid)
            dedup_ids.append(pid)

    dedup_rows.append({
        "query_id": query_id,
        "property_ids": dedup_ids
    })

# ----------------------------
# Save outputs
# ----------------------------
output_dir = BASE_DIR / "global_pool"
output_dir.mkdir(exist_ok=True)

# queries.csv
pd.DataFrame(query_rows).to_csv(
    output_dir / "queries.csv",
    index=False
)

# non-dedup
pd.DataFrame(non_dedup_rows).to_csv(
    output_dir / "global_pool_no_dedup.csv",
    index=False
)

# dedup
pd.DataFrame(dedup_rows).to_csv(
    output_dir / "global_pool_dedup.csv",
    index=False
)

print("✅ Done!")
print(f"Processed {NUM_QUERIES} queries")
print("Files saved in:", output_dir)