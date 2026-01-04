# main_ingest.py
import requests
import json
import csv
import pandas as pd
import openai
from app.storage.connections import get_client
from app.storage.operations import insert_property , insert_objects_with_vectors # your function
# If you also have update_property, can import it similarly
from sentence_transformers import SentenceTransformer

# Load model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


WEAVIATE_URL = "https://your-instance.weaviate.network"
WEAVIATE_API_KEY = "YOUR_WEAVIATE_API_KEY"


OPENROUTER_API_KEY = "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"


DATASET_PATH = "app/storage/test_data.csv"  # path to your CSV
df = pd.read_csv(
    DATASET_PATH,
    encoding="utf-8",      # or "cp1252" if utf-8 fails
    quotechar='"',         # ensures commas/line breaks inside quotes are safe
    delimiter=',',         # CSV delimiter
    engine='python',       # safer parser for complex CSVs
    skip_blank_lines=True  # ignore empty lines
)

# 2️⃣ Clean up column names (remove extra spaces)
df.columns = df.columns.str.strip()

# 3️⃣ Fill missing 'Full Description' with 'Description' if needed
df['Full Description'] = df['Full Description'].fillna(df['Description'])

# 4️⃣ Check parsing
print(df[['id', 'title', 'Full Description']].head())

# -----------------------------
# Property object class
# -----------------------------
# This is a helper to map CSV row to object expected by insert_property
class Property:
    def __init__(self, row):
        self.id = row.get("id")  # can also use UUID or some unique id
        self.url = row.get("url")
        self.title = row.get("title")
        self.location = row.get("location")
        self.latitude = row.get("Latitude")
        self.longitude = row.get("Longitude")
        self.nearest_town = row.get("Nearest Town")
        self.price_lkr = row.get("price_lkr")
        self.price_per_unit = row.get("price_per_unit")
        self.unit = row.get("unit")
        self.price_in_other_currency = row.get("price_in_other_currency")
        self.other_currency = row.get("other_currency")
        self.contract_type = row.get("Contract Type")
        self.property_type = row.get("Property type")
        self.bedrooms = row.get("Bedrooms")
        self.bathrooms = row.get("Bathrooms")
        self.land_size_perches = row.get("Land Size (Perches)")
        self.amenities = row.get("Amenities")
        self.description = row.get("Description")
        self.links_to_image = row.get("Links to Image")
        self.map_link = row.get("Map Link")
        self.full_description = row.get("Full Description")

# -----------------------------
# Main ingestion loop
# -----------------------------

def main():
    data_objects = []
    print(df.head())

    for idx, row in df.iterrows():
        prop = Property(row)
        print("\n\n")
        print(f"reading the property with id {prop.id}")
        print(f"full description: {prop.full_description}")

        # Skip if no text for embedding
        if not prop.full_description:
            print(f"Skipping property {prop.id} due to missing full_description")
            continue

        # Generate vector from full_description
        vector = embedding_model.encode(prop.full_description).tolist()

        # Convert Property object to properties dict
        properties = {
             
            "title": prop.title,
            "location": prop.location,
            "latitude": prop.latitude,
            "longitude": prop.longitude,
            "nearest_town": prop.nearest_town,
            "price_lkr": prop.price_lkr,
            "price_per_unit": prop.price_per_unit,
            "unit": prop.unit,
            "price_in_other_currency": prop.price_in_other_currency,
            "other_currency": prop.other_currency,
            "contract_type": prop.contract_type,
            "property_type": prop.property_type,
            "bedrooms": prop.bedrooms,
            "bathrooms": prop.bathrooms,
            "land_size_perches": prop.land_size_perches,
            "amenities": prop.amenities,
            "description": prop.description,
            "links_to_image": prop.links_to_image,
            "map_link": prop.map_link,
            "full_description": prop.full_description,
        }

        # Build Weaviate object (CORRECT FORMAT)
        data_objects.append(
            {
                "properties": properties,
                "vector": vector
            }
        )
        if prop.id == 3:
            break


    # Batch insert into Weaviate
    insert_objects_with_vectors(
        collection_name="realSearch2",
        data_objects=data_objects
    )

    print(f"Successfully ingested {len(data_objects)} properties into realSearch2")

if __name__ == "__main__":
    main()
