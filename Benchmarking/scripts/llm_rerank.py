import pandas as pd
import json
import google.generativeai as genai
from pathlib import Path
import time

# ----------------------------
# CONFIG
# ----------------------------
genai.configure(api_key="AIzaSyDnhuN3U-1MhFmzOB0dQYmHICGLqLQcJsw")
model = genai.GenerativeModel("gemini-2.5-flash")

BASE_DIR = Path("../outputs/ground_truth")
BASE_DIR.mkdir(parents=True, exist_ok=True)

QUERIES_FILE = "../queries/raw_queries.csv"
POOL_FILE =  "../outputs/global_pool/global_pool_dedup.csv"
PROPERTY_FILE = "../queries/fully_standardized_properties.csv"

TOP_K = 10

# ----------------------------
# BATCH CONTROL (NEW)
# ----------------------------
START_QUERY = 31     # inclusive (1-based index)
END_QUERY = 40      # inclusive
BATCH_SIZE = 10

OUTPUT_FILE = BASE_DIR / f"ground_truth_{START_QUERY}_{END_QUERY}.csv"

# ----------------------------
# Load data
# ----------------------------
queries_df = pd.read_csv(QUERIES_FILE)
pool_df = pd.read_csv(POOL_FILE)
properties_df = pd.read_csv(PROPERTY_FILE)

# ----------------------------
# Speed optimization
# ----------------------------
properties_dict = properties_df.set_index("Property_id").to_dict("index")

# ----------------------------
# Helper: build property text
# ----------------------------
def build_property_text(pid):
    prop = properties_dict.get(pid)
    if not prop:
        return ""

    desc = str(prop.get("Full Description", ""))[:1000]

    return f"""
ID: {pid}
Description: {desc}
"""

# ----------------------------
# Prompt builder
# ----------------------------
def build_prompt(query, property_ids):
    properties_text = "\n\n".join(
        [build_property_text(pid) for pid in property_ids]
    )

    return f"""
You are a real estate search ranking system.

User Query:
{query}

Properties:
{properties_text}

Task:
Select the TOP {TOP_K} most relevant properties.

Rules:
- Focus on matching user intent precisely
- Ignore irrelevant properties
- Prefer better matches even if wording differs

Return EXACTLY {TOP_K} property IDs in ranked order.

Output ONLY JSON array.

Example:
[101, 55, 23]
"""

# ----------------------------
# Retry logic
# ----------------------------
def call_model_with_retry(prompt, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)

        except Exception as e:
            print(f"⚠️ Attempt {attempt+1} failed:", e)

            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return []

# ----------------------------
# Main loop (UPDATED)
# ----------------------------
results = []

start_idx = START_QUERY - 1
end_idx = min(END_QUERY, len(queries_df))

for batch_start in range(start_idx, end_idx, BATCH_SIZE):
    batch_end = min(batch_start + BATCH_SIZE, end_idx)

    print(f"\n🚀 Processing queries {batch_start+1} to {batch_end}")

    for idx in range(batch_start, batch_end):
        query_id = queries_df.iloc[idx]["query_id"]
        query = queries_df.iloc[idx]["query"]

        property_ids = json.loads(pool_df.iloc[idx]["property_ids"])
        property_ids = property_ids[:20]

        prompt = build_prompt(query, property_ids)

        try:
            top_ids = call_model_with_retry(prompt)
        except Exception as e:
            print(f"Error at query {query_id}:", e)
            top_ids = []

        results.append({
            "query_id": query_id,
            "top_10_property_ids": top_ids
        })

        print(f"✅ Done query {query_id}")
        time.sleep(1)

    print(f"✅ Finished batch {batch_start+1}-{batch_end}")
    time.sleep(5)

# ----------------------------
# Save output
# ----------------------------
pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)

print(f"🎉 Ground truth generation complete! Saved to {OUTPUT_FILE}")