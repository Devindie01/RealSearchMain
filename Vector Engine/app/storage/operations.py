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

def apply_filters(query, filters: dict):
    """
    Applies metadata filters to a Weaviate query.
    """
    where = {"operator": "And", "operands": []}

    for field, value in filters.items():
        where["operands"].append({
            "path": [field],
            "operator": "Equal",
            "valueText": value if isinstance(value, str) else None,
            "valueNumber": value if isinstance(value, (int, float)) else None,
        })

    return query.with_where(where)

def query_properties(
    vector: list[float],
    top_k: int = 10,
    radius: float | None = None,
    filters: dict | None = None,
):
    """
    Returns similar properties using vector similarity with optional constraints.
    """
    client = get_client()

    query = client.query.get(
        "Property",
        ["title", "location", "price_lkr", "bedrooms", "bathrooms", "property_type"]
    )

    near_vector = {"vector": vector}
    if radius is not None:
        near_vector["certainty"] = radius

    query = query.with_near_vector(near_vector)
    query = query.with_limit(top_k)

    if filters:
        query = apply_filters(query, filters)

    return query.do()