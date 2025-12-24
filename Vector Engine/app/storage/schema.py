from app.storage.connections import get_client

PROPERTY_SCHEMA = {
    "class": "Property",
    "vectorizer": "none",  # we supply precomputed vectors
    "properties": [
        {"name": "title", "dataType": ["text"]},
        {"name": "location", "dataType": ["text"]},
        {"name": "price_lkr", "dataType": ["number"]},
        {"name": "bedrooms", "dataType": ["int"]},
        {"name": "bathrooms", "dataType": ["int"]},
        {"name": "property_type", "dataType": ["text"]}
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
