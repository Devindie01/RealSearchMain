# from app.models.search import SearchRequest
# from typing import List, Tuple, Dict, Any
# import json

# # Vector Engine Imports
# try:
#     from app.vector_engine.query.executor.query_executor import chain, QueryEmbedder
#     from app.vector_engine.query.formatter import (
#         create_weaviate_filter,
#         execute_search,
#         # execute_weighted_search, # If needed later
#     )
#     from app.vector_engine.query import query_expander
#     from app.vector_engine.storage.connections import get_client
# except ImportError as e:
#     print(f"Warning: Vector Engine imports failed: {e}")
#     # Fallback or allow validation to fail if critical
#     chain = None

# class SearchService:
#     @staticmethod
#     async def search(request: SearchRequest, request_id: str) -> Tuple[List[Dict[str, Any]], int]:
#         # 1. Log behavior
#         print(f"Tracking behavior for request: {request_id}, Query: {request.query}")
        
#         if not chain:
#             return [], 0
            
#         try:
#             # 2. Vector Engine Pipeline
            
#             # A. Query Expansion
#             user_input = request.query
#             new_query = query_expander.get_query_expansion(user_input)
#             expaned_query = new_query["expanded_query"]
#             weights = new_query["scaled_weights"]
            
#             # For now, let's keep it simple or follow the main.py logic strictly?
#             # main.py does expansion -> extraction -> embedding -> filter -> search
            
#             user_input = request.query
#             print(f"Processing query: {user_input}")

#             # Query expansion
#             new_query = query_expander.get_query_expansion(user_input)
#             expaned_query = new_query["expanded_query"]
#             # weights = new_query["scaled_weights"] # Used in weighted search

#             # B. Extract structured data using the LLM chain
#             result_segment = chain.invoke({"input": expaned_query})
            
#             # C. Generate vector embedding
#             embedder = QueryEmbedder()
#             query_vector = embedder.get_vector(result_segment.description)
            
#             # D. Format Weaviate filters
#             wv_filter = create_weaviate_filter(result_segment) # create_weaviate_filter might not be compatible with Weaviate Client 4.x v3.x differences if any.
#             # But we are importing it from existing code, so it should be fine.
            
#             # E. Execute Search
#             print("Executing search on Weaviate...")
#             results = []
#             with get_client() as client:
#                 # execute_search expects: (user_query, vector, structured_segment, client)
#                 results_objs = execute_search(user_input, query_vector, result_segment, client)
                
#                 # Convert Weaviate objects to Dicts matching our schema
#                 if results_objs:
#                     for obj in results_objs:
#                         # Assuming obj.properties is a dict
#                         prop = obj.properties
#                         results.append({
#                             "title": prop.get('title', 'N/A'),
#                             "description": prop.get('description', 'N/A'),
#                             "property_type": prop.get('property_type', 'N/A'),
#                             "contract_type": prop.get('contract_type', 'N/A'), # Verify field name
#                             "price_lkr": prop.get('price_lkr', 0),
#                             "location": prop.get('location', 'N/A'),
#                             "owner_id": prop.get('owner_id', 0), # Might not be in vector DB?
#                             "score": 0.0 # obj.metadata.score if available
#                         })

#             return results, len(results)

#         except Exception as e:
#             print(f"Error in vector search pipeline: {e}")
#             return [], 0

