from app.storage.connections import get_client

with get_client() as client:
    # 1. Access the collection
    collection = client.collections.get("RealSearch")

    # 2. Fetch the configuration
    config = collection.config.get()

    print(f"\n--- Schema for Collection: {config.name} ---")
    for prop in config.properties:
        print(f"Property: '{prop.name}' | Data Type: {prop.data_type}")


def fetch_sample_data():
    with get_client() as client:
        # 1. Access the collection
        collection = client.collections.get("RealSearch")

        # 2. Fetch the first 5 objects
        # We include 'include_vector=False' to keep the printout clean
        response = collection.query.fetch_objects(limit=5)

        print(f"\n--- Top 5 Records from {collection.name} ---\n")

        if not response.objects:
            print("No data found in the collection.")
            return

        for i, obj in enumerate(response.objects, 1):
            props = obj.properties
            print(f"Record {i}:")
            print(f"  Title:    {props.get('title')}")
            print(f"  Location: {props.get('location')}")
            print(f"  Price:    {props.get('priceLkr')}")
            print(f"  Type:     {props.get('propertyType')}")
            print(f"  Bedrooms: {props.get('bedrooms')}")
            print("-" * 30)


print("\n--- Sample Data ---\n")
fetch_sample_data()
