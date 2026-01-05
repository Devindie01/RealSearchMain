from app.storage.connections import get_client

with get_client() as client:
    # 1. Access the collection
    collection = client.collections.get("RealSearch")

    # 2. Fetch the configuration
    config = collection.config.get()

    print(f"\n--- Schema for Collection: {config.name} ---")
    for prop in config.properties:
        print(f"Property: '{prop.name}' | Data Type: {prop.data_type}")
