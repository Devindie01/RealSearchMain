import pandas as pd
import json
import google.generativeai as genai
from pathlib import Path
import time

# ----------------------------
# CONFIG
# ----------------------------
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-2.5-flash")

BASE_DIR = Path("../outputs/global_pool")

QUERIES_FILE = BASE_DIR / "queries.csv"
POOL_FILE = BASE_DIR / "global_pool_dedup.csv"
PROPERTY_FILE = "../data/properties.csv"   # adjust if needed

OUTPUT_FILE = BASE_DIR / "ground_truth.csv"

TOP_K = 10

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

    desc = str(prop.get("Full Description", ""))[:1000]  # truncate for safety

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
# Main loop
# ----------------------------
results = []

for idx in range(len(queries_df)):
    query_id = queries_df.iloc[idx]["query_id"]
    query = queries_df.iloc[idx]["query"]

    property_ids = json.loads(pool_df.iloc[idx]["property_ids"])

    # optional safety limit (recommended)
    property_ids = property_ids[:20]

    prompt = build_prompt(query, property_ids)

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        text = text.replace("```json", "").replace("```", "").strip()
        top_ids = json.loads(text)

    except Exception as e:
        print(f"Error at query {query_id}:", e)
        top_ids = []

    results.append({
        "query_id": query_id,
        "top_10_property_ids": top_ids
    })

    print(f"✅ Done query {query_id}")

    time.sleep(1)

# ----------------------------
# Save output
# ----------------------------
pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)

print("🎉 Ground truth generation complete!")