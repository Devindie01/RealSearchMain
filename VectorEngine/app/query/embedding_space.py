from app.query.executor.query_executor import initialize_chain, QueryEmbedder

def process_user_query(user_input):
    # 1. Get the structured result from your LLM (as you already did)
    chain = initialize_chain()
    result = chain.invoke({"input": user_input})

    # 2. Initialize the embedder
    embedder = QueryEmbedder()

    # 3. Vectorize ONLY the description part
    query_vector = embedder.get_vector(result.description)

    # Now you have:
    # - result.no_of_bedrooms (Integer for filtering)
    # - result.price (Float for filtering)
    # - query_vector (List of floats for vector search)
    return result, query_vector