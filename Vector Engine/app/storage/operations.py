from app.storage.connections import get_client


def insert_property(property_obj, vector: list[float]):
    """
    Inserts a property into the vector DB with metadata and aggregated vector.
    """
    client = get_client()

    data_object = {
            "url": property_obj.url,
            "title": property_obj.title,
            "location": property_obj.location,
            "latitude": property_obj.latitude,
            "longitude": property_obj.longitude,
            "nearest_town": getattr(property_obj, "nearest_town", None),
            "price_lkr": property_obj.price_lkr,
            "price_per_unit": getattr(property_obj, "price_per_unit", None),
            "unit": getattr(property_obj, "unit", None),
            "price_in_other_currency": getattr(property_obj, "price_in_other_currency", None),
            "other_currency": getattr(property_obj, "other_currency", None),
            "contract_type": getattr(property_obj, "contract_type", None),
            "property_type": property_obj.property_type,
            "bedrooms": getattr(property_obj, "bedrooms", None),
            "bathrooms": getattr(property_obj, "bathrooms", None),
            "land_size_perches": getattr(property_obj, "land_size_perches", None),
            "amenities": getattr(property_obj, "amenities", None),
            "description": getattr(property_obj, "description", None),
            "links_to_image": getattr(property_obj, "links_to_image", None),
            "map_link": getattr(property_obj, "map_link", None),
         }
    client.data_object.create(
        data_object= data_object,
        class_name="Property",
        vector=vector,
        uuid=property_obj.id,
    )


def update_property(property_obj, vector: list[float]):
    """
    Updates an existing property vector or metadata.
    """
    client = get_client()
    data_object = {
            "url": property_obj.url,
            "title": property_obj.title,
            "location": property_obj.location,
            "latitude": property_obj.latitude,
            "longitude": property_obj.longitude,
            "nearest_town": getattr(property_obj, "nearest_town", None),
            "price_lkr": property_obj.price_lkr,
            "price_per_unit": getattr(property_obj, "price_per_unit", None),
            "unit": getattr(property_obj, "unit", None),
            "price_in_other_currency": getattr(property_obj, "price_in_other_currency", None),
            "other_currency": getattr(property_obj, "other_currency", None),
            "contract_type": getattr(property_obj, "contract_type", None),
            "property_type": property_obj.property_type,
            "bedrooms": getattr(property_obj, "bedrooms", None),
            "bathrooms": getattr(property_obj, "bathrooms", None),
            "land_size_perches": getattr(property_obj, "land_size_perches", None),
            "amenities": getattr(property_obj, "amenities", None),
            "description": getattr(property_obj, "description", None),
            "links_to_image": getattr(property_obj, "links_to_image", None),
            "map_link": getattr(property_obj, "map_link", None),

        }
    client.data_object.update(
        data_object= data_object,
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