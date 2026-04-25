import pandas as pd
import json
import time
from openai import OpenAI
from pathlib import Path

# ----------------------------
# CONFIG
# ----------------------------
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",  # ← replace with your OpenRouter API key
)
MODEL = "meta-llama/llama-3.3-70b-instruct"  # great at paraphrasing, cheap, fast

QUERIES_FILE = "../queries/raw_queries.csv"         # ← your input queries CSV
OUTPUT_FILE  = "../outputs/augmented_queries.csv"        # ← output file

AUGMENTATIONS_PER_QUERY = 5  # how many variants to generate per query
MAX_TOKENS = 1024
RETRY_DELAY = 5
MAX_RETRIES = 3
QUERY_DELAY = 1.0             # seconds between API calls


# ----------------------------
# Prompt
# ----------------------------
SYSTEM_PROMPT = """You are a data augmentation assistant for a real estate search dataset.
Your job is to rephrase real estate search queries while preserving ALL factual details with 100% accuracy.

STRICT RULES — never violate these:
- Location names must be IDENTICAL (same spelling, same area)
- Number of bedrooms and bathrooms must be IDENTICAL
- Budget/price figures must be IDENTICAL
- Dates and durations must be IDENTICAL
- Property type (house/villa/land/apartment) must be IDENTICAL
- Any specific requirements (beach distance, legal status, furnishings, etc.) must be IDENTICAL

What you CAN change:
- Sentence structure and word order
- Formal vs. casual tone
- Bullet points ↔ prose paragraph style
- Emoji usage (add or remove)
- Language formality (e.g. "I'm looking for" → "Seeking" → "Wanted:")
- Greeting/closing phrases
- Active vs. passive voice

Output ONLY a valid JSON array of strings. No explanation, no markdown.

Example input:
"Looking for a 3 bedroom house to rent in Galle. Budget: 100,000 LKR/month."

Example output (5 variants):
[
  "Wanted: 3-bedroom rental house in Galle. Monthly budget up to LKR 100,000.",
  "Hi, I need to rent a house in Galle with 3 bedrooms. My budget is 100,000 LKR per month.",
  "3BR house for rent in Galle — budget 100k LKR/month. Anyone know of something available?",
  "Seeking a 3-bedroom apartment for rent in Galle. Budget: 100,000 LKR/month.",
  "I'm looking for a house in Galle with 3 bedrooms. My budget is 100,000 LKR per month."
]"""


def build_user_prompt(query, n):
    return f"""Generate exactly {n} rephrased versions of the following real estate query.
Remember: locations, bedroom/bathroom counts, budget, dates, and property type must stay 100% identical.

Query:
{query}

Return ONLY a JSON array of exactly {n} strings."""


# ----------------------------
# Retry logic
# ----------------------------
def augment_query(query_text, n=AUGMENTATIONS_PER_QUERY):
    for attempt in range(1, MAX_RETRIES + 1):
        print("\n\n")
        print("Query:", query_text)
        
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": build_user_prompt(query_text, n)},
                ],
                max_tokens=MAX_TOKENS,
                temperature=0.8,   # some creativity but controlled
            )
            text = response.choices[0].message.content.strip()
            text = text.replace("```json", "").replace("```", "").strip()
            variants = json.loads(text)

            if not isinstance(variants, list):
                raise ValueError("Response is not a list")

            # Ensure we got the right number of variants
            variants = variants[:n]
            print(f"  ✓ Successfully generated {len(variants)} variants.")
            print("  Variants:", variants)
            return variants

        except Exception as e:
            print(f"  ⚠ Attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                print(f"  ✗ Skipping query after {MAX_RETRIES} failed attempts.")
                return []


# ----------------------------
# Main
# ----------------------------
queries_df = pd.read_csv(QUERIES_FILE)
print(f"Loaded {len(queries_df)} queries from {QUERIES_FILE}")

augmented_rows = []

for idx, row in queries_df.iterrows():
    query_id   = row["query_id"]
    query_text = str(row["query"])

    # Skip placeholder rows
    if query_text.strip().lower() in ["original", "nan", ""]:
        print(f"[{idx+1}/{len(queries_df)}] query_id={query_id} — skipped (placeholder)")
        continue

    print(f"[{idx+1}/{len(queries_df)}] query_id={query_id} — augmenting...")

    variants = augment_query(query_text)

    for v_idx, variant in enumerate(variants, start=1):
        augmented_rows.append({
            "original_query_id": query_id,
            "augmented_query_id": f"{query_id}_aug{v_idx}",
            "original_query": query_text,
            "augmented_query": variant,
        })
        print(f"  ✓ variant {v_idx}: {variant[:80]}...")

    time.sleep(QUERY_DELAY)

# ----------------------------
# Save
# ----------------------------
out_df = pd.DataFrame(augmented_rows)
out_df.to_csv(OUTPUT_FILE, index=False)

print(f"\n🎉 Done! {len(augmented_rows)} augmented queries saved to {OUTPUT_FILE}")
print(f"   Original queries: {len(queries_df)}")
print(f"   Augmented queries: {len(augmented_rows)}")