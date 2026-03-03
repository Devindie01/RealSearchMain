import weaviate.classes as wvc
from weaviate.classes.query import Filter, HybridFusion
from app.query.executor.query_executor import QuerySegment
from app.query.formatter import create_weaviate_filter

def get_alpha_from_srr(classification):
    """
    Logic: If SRR is high (lots of entities, little leftover), we lean toward Keyword/Metadata (alpha -> 0).
    If SRR is low (few entities, lots of natural language), we lean toward Vector (alpha -> 1).
    """
    srr = classification.get("SRR", 1)
    if srr == float('inf'):
        return 0.0  # Purely structured
    
    # Simple Inverse Mapping: High SRR -> Low Alpha
    # You can tune this formula based on your testing
    alpha = 1 / (1 + srr) 
    return round(alpha, 2)

def execute_search(user_input, query_vector, result_segment, client, alpha):
    # 1. Get the collection
    houses = client.collections.get("RealSearch")

    # 2. Build the filter
    wv_filter = create_weaviate_filter(result_segment)

    # 3. Perform Hybrid Search
    response = houses.query.hybrid(
        query=user_input,  # For BM25 keyword search
        vector=query_vector,  # For Vector semantic search
        filters=wv_filter,  # Our "Hard" metadata filters
        alpha=alpha,  # Balance (0=keyword, 1=vector)
        limit=5,
    )

    return response.objects