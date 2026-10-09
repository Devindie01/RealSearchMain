from warnings import filters

import weaviate
import weaviate.classes as wvc
from functools import reduce
from weaviate.classes.query import Filter, HybridFusion
from app.query.query_object import QuerySegment


def create_weaviate_filter(segment: QuerySegment):
    filters = []

    if segment.property_type:
        types = segment.property_type

        if isinstance(types, str):
            types = [types]

        type_filters = [Filter.by_property("propertyType").equal(t) for t in types if t]

        if len(type_filters) == 1:
            filters.append(type_filters[0])

        elif len(type_filters) > 1:
            combined = reduce(lambda a, b: a | b, type_filters)
            filters.append(combined)

    if segment.contract_type:
        filters.append(Filter.by_property("contractType").equal(segment.contract_type))

    if segment.price_max:
        if segment.price_unit.upper() == "LKR":
            filters.append(
                Filter.by_property("priceUnit").less_or_equal(segment.price_unit)
            )
        else:
            # use exchange rate to convert to LKR and filter
            filters.append(
                Filter.by_property("priceLKR").less_or_equal(segment.price_max)
            )

    if segment.location:
        locs = (
            segment.location
            if isinstance(segment.location, list)
            else [segment.location]
        )

        loc_filters = [Filter.by_property("location").equal(loc) for loc in locs if loc]

        if len(loc_filters) == 1:
            filters.append(loc_filters[0])
        elif len(loc_filters) > 1:
            combined = reduce(lambda a, b: a | b, loc_filters)
            filters.append(combined)

    if segment.no_of_bedrooms:
        filters.append(Filter.by_property("bedrooms").equal(segment.no_of_bedrooms))

    if segment.no_of_bathrooms:
        filters.append(Filter.by_property("bathrooms").equal(segment.no_of_bathrooms))

    if segment.land_size:
        filters.append(
            Filter.by_property("landSize").greater_or_equal(segment.land_size)
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
    houses = client.collections.get("RealSearchPropData")

    # 2. Build the filter
    wv_filter = create_weaviate_filter(result_segment)

    # 3. Perform Hybrid Search
    response = houses.query.hybrid(
        query=user_input,  # For BM25 keyword search
        vector=query_vector,  # For Vector semantic search
        filters=wv_filter,  # Our "Hard" metadata filters
        alpha=0.4,  # Balance (0=keyword, 1=vector)
        limit=5,
    )

    return response.objects


# 1. Take your DSPy or LLM weights
# Example weights: {'location': 3, 'property_type': 2, 'description': 1}


def execute_weighted_search(user_query, query_vector, weights, client):
    collection = client.collections.get("RealSearchPropData")

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
        limit=5,
    )
    return response.objects
