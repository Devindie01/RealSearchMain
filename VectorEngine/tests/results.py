import pandas as pd
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.storage.connections import get_client
from tests.pipeline import run_pipeline_test


def process_queries_to_file(csv_path, output_path):
    # 1. Load the CSV
    # Ensure the column name matches your CSV header (e.g., 'Semantic')
    df = pd.read_csv(csv_path)
    queries = df["Original"].tolist()

    results_map = {}

    with get_client() as client:
        for q in queries[0:10]:
            if pd.isna(q):
                continue  # Skip empty rows

            try:
                # 2. Run your pipeline
                # Assuming run_pipeline_test returns a list of property objects/dicts
                retrieved_properties = run_pipeline_test(q, client)

                # 3. Store in dictionary
                results_map[q] = retrieved_properties

            except Exception as e:
                print(f"Error processing '{q}': {e}")

                results_map[q] = f"Error: {str(e)}"

    # 4. Save to a JSON file (Key-Value format)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results_map, f, indent=4, ensure_ascii=False)

    print(f"\nDone! Results saved to {output_path}")


# Configuration
csv_file_path = (
    r"D:\FYP\RealSearch\VectorEngine\query_data\RealSearch Leads - Queries.csv"
)
output_file_path = "retrieved_results.json"

# Execute
process_queries_to_file(csv_file_path, output_file_path)
