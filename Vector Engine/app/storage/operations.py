from app.storage.connections import get_client


def insert_property(property_obj, vector: list[float]):
    """
    Inserts a property into the vector DB with metadata and aggregated vector.
    """
    client = get_client()
    client.data_object.create(
        data_object={
            "title": property_obj.title,
            "location": property_obj.location,
            "price_lkr": property_obj.price_lkr,
            "bedrooms": property_obj.bedrooms,
            "bathrooms": property_obj.bathrooms,
            "property_type": property_obj.property_type,
        },
        class_name="Property",
        vector=vector,
        uuid=property_obj.id,
    )


def update_property(property_obj, vector: list[float]):
    """
    Updates an existing property vector or metadata.
    """
    client = get_client()
    client.data_object.update(
        data_object={
            "title": property_obj.title,
            "location": property_obj.location,
            "price_lkr": property_obj.price_lkr,
            "bedrooms": property_obj.bedrooms,
            "bathrooms": property_obj.bathrooms,
            "property_type": property_obj.property_type,
        },
        class_name="Property",
        uuid=property_obj.id,
        vector=vector,
    )


def query_properties(vector: list[float], top_k: int = 10, filters: dict = None):
    """
    Returns top_k similar properties based on vector similarity.
    filters: optional dictionary to filter metadata fields
    """
    client = get_client()
    query = client.query.get(
        "Property", ["title", "location", "price_lkr", "bedrooms", "bathrooms"]
    )
    query = query.with_near_vector({"vector": vector, "certainty": 0.7})
    query = query.with_limit(top_k)
    # TODO: Apply filters if needed
    results = query.do()
    return results
