import pandas as pd
import json
from openai import OpenAI
from pathlib import Path
import time

# ----------------------------
# CONFIG
# ----------------------------
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",  # ← replace with your OpenRouter API key
)

MODEL = "google/gemini-2.5-flash"

BASE_DIR = Path("../outputs/ground_truth")
BASE_DIR.mkdir(parents=True, exist_ok=True)

QUERIES_FILE = "../queries/raw_queries.csv"
POOL_FILE =  "../outputs/global_pool/global_pool_dedup.csv"
PROPERTY_FILE = "../queries/fully_standardized_properties.csv"

TOP_K = 10

# ----------------------------
# BATCH CONTROL
# ----------------------------
START_QUERY = 101     # inclusive (1-based index)
END_QUERY = 207    # inclusive
BATCH_SIZE = 108

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
    print(f"🔍 Building prompt for query: '{query}' with {len(property_ids)} properties")
    print(f"📄 Sample property text:\n{properties_text[:500]}...")  # Print a sample of the properties text
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
- Prefer better matches even if wording differs
- You MUST always return EXACTLY {TOP_K} property IDs — no more, no less
- If there are not enough perfect matches, rank the remaining properties by best partial match and include them anyway
- Never return fewer than {TOP_K} results
 
Return EXACTLY {TOP_K} property IDs in ranked order.
 
Output ONLY a JSON array with exactly {TOP_K} integers. No explanation.
 
Example:
when top k = 10
[101, 55, 23 , ... up to 10 IDs ...]
"""

# ----------------------------
# Retry logic
# ----------------------------
def call_model_with_retry(prompt, retries=3, delay=5):
    for attempt in range(retries):
        print(f"🤖 Calling model (Attempt {attempt+1}/{retries})...")
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )
            text = response.choices[0].message.content.strip()
            text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)

        except Exception as e:
            print(f"⚠️ Attempt {attempt+1} failed:", e)

            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return []

# ----------------------------
# Main loop
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