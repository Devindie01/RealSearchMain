from app.storage.connections import get_client

PROPERTY_SCHEMA = {
    "class": "Property",
    "vectorizer": "none",
    "properties": [
        {"name": "url", "dataType": ["text"]},
        {"name": "title", "dataType": ["text"]},
        {"name": "location", "dataType": ["text"]},
        {"name": "latitude", "dataType": ["number"]},
        {"name": "longitude", "dataType": ["number"]},
        {"name": "nearest_town", "dataType": ["text"]},
        {"name": "price_lkr", "dataType": ["number"]},
        {"name": "price_per_unit", "dataType": ["text"]},
        {"name": "unit", "dataType": ["text"]},
        {"name": "price_in_other_currency", "dataType": ["number"]},
        {"name": "other_currency", "dataType": ["text"]},
        {"name": "contract_type", "dataType": ["text"]},
        {"name": "property_type", "dataType": ["text"]},
        {"name": "bedrooms", "dataType": ["int"]},
        {"name": "bathrooms", "dataType": ["int"]},
        {"name": "land_size_perches", "dataType": ["number"]},
        {"name": "amenities", "dataType": ["text[]"]},  # array of strings
        {"name": "description", "dataType": ["text"]},
        {"name": "links_to_image", "dataType": ["text[]"]},  # array of image URLs
        {"name": "map_link", "dataType": ["text"]},
        {"name": "full_description", "dataType": ["text"]}
    ]
}

def create_schema():
    client = get_client()
    # Check if class exists before creating
    if not client.schema.contains({"class": "Property"}):
        client.schema.create_class(PROPERTY_SCHEMA)
        print("Property schema created.")
    else:
        print("Property schema already exists.")
