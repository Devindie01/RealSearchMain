import pandas as pd
import json
import glob
import os

# ----------------------------
# CONFIG
# ----------------------------
AUGMENTED_FILE     = "../outputs/augmented_queries.csv"    # original_query_id, augmented_query_id, original_query, augmented_query
GROUND_TRUTH_DIR   = "../outputs/ground_truth/"           # folder containing all ground_truth_*.csv files
OUTPUT_FILE        = "../outputs/merged_dataset.csv"


# ----------------------------
# Load & combine all ground truth CSVs
# ----------------------------
gt_files = sorted(glob.glob(os.path.join(GROUND_TRUTH_DIR, "ground_truth_*.csv")))
print(f"Found {len(gt_files)} ground truth files:")
for f in gt_files:
    print(f"  {f}")

gt_df = pd.concat([pd.read_csv(f) for f in gt_files], ignore_index=True)
print(f"\nTotal ground truth rows: {len(gt_df)}")

# Build lookup: original_query_id -> results list
gt_lookup = {}
for _, row in gt_df.iterrows():
    qid = int(row["query_id"])
    try:
        results = json.loads(str(row["top_10_property_ids"]))
    except Exception:
        results = []
    gt_lookup[qid] = results


# ----------------------------
# Load augmented queries
# ----------------------------
aug_df = pd.read_csv(AUGMENTED_FILE)
print(f"\nAugmented queries loaded: {len(aug_df)}")


# ----------------------------
# Build rows
# ----------------------------
rows = []

# Row 1: "Original" placeholder (query_id=1)
rows.append({
    "original_query_id" : 1,
    "query_id"          : 1,
    "query"             : "Original",
    "results"           : json.dumps([]),
})

# Original queries (unique original_query_id + original_query)
originals = (
    aug_df[["original_query_id", "original_query"]]
    .drop_duplicates(subset="original_query_id")
    .sort_values("original_query_id")
)

for _, row in originals.iterrows():
    qid   = int(row["original_query_id"])
    query = str(row["original_query"])

    if qid == 1:  # already added above
        continue

    rows.append({
        "original_query_id" : qid,
        "query_id"          : qid,
        "query"             : query,
        "results"           : json.dumps(gt_lookup.get(qid, [])),
    })

print(f"Original rows built : {len(rows)} (including placeholder)")

# Augmented queries
aug_count = 0
for _, row in aug_df.iterrows():
    original_qid = int(row["original_query_id"])
    aug_qid      = str(row["augmented_query_id"])   # e.g. "42_aug1"
    aug_query    = str(row["augmented_query"])

    rows.append({
        "original_query_id" : original_qid,
        "query_id"          : aug_qid,
        "query"             : aug_query,
        "results"           : json.dumps(gt_lookup.get(original_qid, [])),
    })
    aug_count += 1

print(f"Augmented rows built: {aug_count}")


# ----------------------------
# Assemble final dataframe
# ----------------------------
merged_df = pd.DataFrame(rows, columns=["original_query_id", "query_id", "query", "results"])

# Add sequential new_query_id as the first column
merged_df.insert(0, "new_query_id", range(1, len(merged_df) + 1))

merged_df.to_csv(OUTPUT_FILE, index=False)

print(f"\nDone! Total rows : {len(merged_df)}")
print(f"   Saved to        : {OUTPUT_FILE}")
print(f"\nSample (first 5 rows):")
print(merged_df.head(5).to_string(index=False))
print(f"\nSample (first 3 augmented rows):")
aug_sample = merged_df[merged_df["query_id"].astype(str).str.contains("_aug")].head(3)
print(aug_sample.to_string(index=False))