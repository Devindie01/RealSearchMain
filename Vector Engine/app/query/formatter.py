import weaviate
import weaviate.classes as wvc
from weaviate.classes.query import Filter,HybridFusion
from app.query.executor.query_executor import QuerySegment


def create_weaviate_filter(segment: QuerySegment):
    filters = []

    if segment.property_type:
        filters.append(Filter.by_property("property_type").equal(segment.property_type))

    if segment.contract_type:
        filters.append(Filter.by_property("contract_type").equal(segment.contract_type))

    if segment.price:
        filters.append(Filter.by_property("price").less_or_equal(segment.price))

    if segment.location:
        filters.append(Filter.by_property("location").equal(segment.location))

    if segment.no_of_bedrooms:
        filters.append(
            Filter.by_property("no_of_bedrooms").equal(segment.no_of_bedrooms)
        )

    if segment.no_of_bathrooms:
        filters.append(
            Filter.by_property("no_of_bathrooms").equal(segment.no_of_bathrooms)
        )

    if segment.land_size:
        filters.append(
            Filter.by_property("land_size").greater_or_equal(segment.land_size)
        )

    # Combine all filters using AND logic (&)
    if not filters:
        return None

    combined_filter = filters[0]
    for f in filters[1:]:
        combined_filter = combined_filter & f

    return combined_filter


def execute_search(user_input, query_vector, result_segment, client):
    # 1. Get the collection
    houses = client.collections.get("Properties")

    # 2. Build the filter
    wv_filter = create_weaviate_filter(result_segment)

    # 3. Perform Hybrid Search
    response = houses.query.hybrid(
        query=user_input,  # For BM25 keyword search
        vector=query_vector,  # For Vector semantic search
        filters=wv_filter,  # Our "Hard" metadata filters
        fusion_type=HybridFusion.RELATIVE_SCORE,
        query_properties=[
            "location^4",
            "price^4",
            "contract_type^4",
            "property_type^3",
            "description^1",
        ],
        alpha=0.4,  # Balance (0=keyword, 1=vector)
        limit=5,
    )

    return response.objects

# 1. Take your DSPy or LLM weights
# Example weights: {'location': 3, 'property_type': 2, 'description': 1}

def execute_weighted_search(user_query, query_vector, weights, client):
    collection = client.collections.get("Properties")
    
    # 2. Convert weights into Weaviate's "Property Boosting" format
    # This creates a list like ["location^3", "property_type^2", "description^1"]
    boosted_properties = [f"{prop}^{weight}" for prop, weight in weights.items()]

    response = collection.query.hybrid(
        query=user_query,
        vector=query_vector,
        fusion_type=HybridFusion.RELATIVE_SCORE,
        # WEAVIATE WEIGHTS APPLIED HERE
        query_properties=boosted_properties, 
        alpha=0.5,
        limit=5
    )
    return response.objects
