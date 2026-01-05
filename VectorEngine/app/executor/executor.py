from storage.operations import query_properties
from executor.search_params import SearchParams

class SearchExecutor:
    def execute(self, query_vector, intent):
        filters = {}

        if intent.category_filter:
            filters["property_type"] = intent.category_filter

        search_params = SearchParams(
            top_k=10,
            radius=0.7,
            filters=filters
        )

        results = query_properties(
            vector=query_vector.tolist(),
            top_k=search_params.top_k,
            radius=search_params.radius,
            filters=search_params.filters,
        )

        return results
