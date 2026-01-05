from app.storage.connections import get_client
import weaviate
from weaviate.classes.config import Configure
from app.storage.config import  WEAVIATE_URL , WEAVIATE_API_KEY
from weaviate.classes.init import AdditionalConfig, Timeout, Auth
from weaviate.classes.query import Filter

# function to create a collection, then stote data objects with vectors

def insert_objects_with_vectors(
    collection_name: str,
    data_objects: list[dict],
    batch_size: int = 200,
):
    """
    Inserts data objects with vectors into a Weaviate collection.

    Each data object must be in the format:
    {
        "properties": {...},
        "vector": [float, float, ...]
    }
    """

    weaviate_url = WEAVIATE_URL
    weaviate_api_key =  WEAVIATE_API_KEY

    with weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=weaviate_api_key,
    ) as client:

        # Create collection if it does not exist
        if not client.collections.exists(collection_name):
            client.collections.create(
                name=collection_name,
                vector_config=Configure.Vectors.self_provided(),
            )

        collection = client.collections.get(collection_name)

        # Batch insert objects
        with collection.batch.fixed_size(batch_size=batch_size) as batch:
            for obj in data_objects:
                batch.add_object(
                    properties=obj["properties"],
                    vector=obj["vector"],
                )

        print(
            f"Imported {len(data_objects)} objects with vectors into the '{collection_name}' collection"
        )



def search_real_search_collection(query_text: str, limit: int = 3):
    """
    Connects to Weaviate, accesses 'RealSearch', and retrieves data using vector search.
    """

    # 1. Retrieve environment variables
    url =  WEAVIATE_URL
    api_key =  WEAVIATE_API_KEY

    if not url or not api_key:
        print("Error: WEAVIATE_URL or WEAVIATE_API_KEY is missing.")
        return

    # 2. Connect using a Context Manager (automatically closes connection after use)
    try:
        with weaviate.connect_to_weaviate_cloud(
            cluster_url=url,
            auth_credentials=Auth.api_key(api_key),
            additional_config=AdditionalConfig(timeout=Timeout(init=10)),
        ) as client:

            # 3. Check if collection exists before querying
            if not client.collections.exists("RealSearch"):
                print(f"Collection 'RealSearch' does not exist in this cluster.")
                return

            # 4. Get the collection
            real_search_collection = client.collections.get("RealSearch")

            # 5. Perform the query
            # We use 'near_text' for semantic search.
            # If you just want to list data without similarity, use .fetch_objects()
            response = real_search_collection.query.near_text(
                query=query_text,
                limit=limit
            )

            # 6. Process and return/print results
            results = []
            for obj in response.objects:
                # obj.properties contains the data fields
                results.append(obj.properties)
#                 print(f"Found: {obj.properties}")

            return results

    except Exception as e:
        print(f"An error occurred: {e}")

def search_real_search_collection_with_filters(query_text: str, filters=None, limit: int = 3):
    """
    Connects to Weaviate and searches 'RealSearch'.

    Args:
        query_text: The text to search for semantically.
        filters: A Weaviate Filter object (optional).
        limit: Number of results to return.
    """
    url =  WEAVIATE_URL
    api_key =  WEAVIATE_API_KEY

    if not url or not api_key:
        print("Error: WEAVIATE_URL or WEAVIATE_API_KEY is missing.")
        return

    try:
        with weaviate.connect_to_weaviate_cloud(
            cluster_url=url,
            auth_credentials=Auth.api_key(api_key),
            additional_config=AdditionalConfig(timeout=Timeout(init=10)),
        ) as client:

            # Check if collection exists
            if not client.collections.exists("RealSearch"):
                print("Collection 'RealSearch' not found.")
                return

            real_search = client.collections.get("RealSearch")

            # Perform query with the passed 'filters'
            response = real_search.query.near_text(
                query=query_text,
                limit=limit,
                filters=filters  # <--- Filters are applied here if provided
            )

            results = []
            for obj in response.objects:
                results.append(obj.properties)
                # Printing title and location for quick verification
                title = obj.properties.get('title', 'No Title')
                town = obj.properties.get('nearestTown', 'Unknown')
                print(f"Found: {title} | Town: {town}")

            return results

    except Exception as e:
        print(f"An error occurred: {e}")
# def insert_property(property_obj, vector: list[float]):
#     """
#     Inserts a property into the vector DB with metadata and vector.
#     """
#     client = get_client()
#     try:
#         collection = client.collections.get("Property")
#
#         data_object = {
#             "url": property_obj.url,
#             "title": property_obj.title,
#             "location": property_obj.location,
#             "latitude": property_obj.latitude,
#             "longitude": property_obj.longitude,
#             "nearest_town": getattr(property_obj, "nearest_town", None),
#             "price_lkr": property_obj.price_lkr,
#             "price_per_unit": getattr(property_obj, "price_per_unit", None),
#             "unit": getattr(property_obj, "unit", None),
#             "price_in_other_currency": getattr(property_obj, "price_in_other_currency", None),
#             "other_currency": getattr(property_obj, "other_currency", None),
#             "contract_type": getattr(property_obj, "contract_type", None),
#             "property_type": property_obj.property_type,
#             "bedrooms": getattr(property_obj, "bedrooms", None),
#             "bathrooms": getattr(property_obj, "bathrooms", None),
#             "land_size_perches": getattr(property_obj, "land_size_perches", None),
#             "amenities": getattr(property_obj, "amenities", None),
#             "description": getattr(property_obj, "description", None),
#             "links_to_image": getattr(property_obj, "links_to_image", None),
#             "map_link": getattr(property_obj, "map_link", None),
#         }
#
#         collection.data.insert(
#             properties=data_object,
#             vector=vector,
#             uuid=property_obj.id
#         )
#
#     finally:
#         client.close()
#

# def update_property(property_obj, vector: list[float]):
#     """
#     Updates an existing property vector or metadata.
#     """
#     client = get_client()
#     data_object = {
#             "url": property_obj.url,
#             "title": property_obj.title,
#             "location": property_obj.location,
#             "latitude": property_obj.latitude,
#             "longitude": property_obj.longitude,
#             "nearest_town": getattr(property_obj, "nearest_town", None),
#             "price_lkr": property_obj.price_lkr,
#             "price_per_unit": getattr(property_obj, "price_per_unit", None),
#             "unit": getattr(property_obj, "unit", None),
#             "price_in_other_currency": getattr(property_obj, "price_in_other_currency", None),
#             "other_currency": getattr(property_obj, "other_currency", None),
#             "contract_type": getattr(property_obj, "contract_type", None),
#             "property_type": property_obj.property_type,
#             "bedrooms": getattr(property_obj, "bedrooms", None),
#             "bathrooms": getattr(property_obj, "bathrooms", None),
#             "land_size_perches": getattr(property_obj, "land_size_perches", None),
#             "amenities": getattr(property_obj, "amenities", None),
#             "description": getattr(property_obj, "description", None),
#             "links_to_image": getattr(property_obj, "links_to_image", None),
#             "map_link": getattr(property_obj, "map_link", None),
#
#         }
#     client.data_object.update(
#         data_object= data_object,
#         class_name="Property",
#         uuid=property_obj.id,
#         vector=vector,
#     )

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