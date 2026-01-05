import json
from app.query.executor.query_executor import chain, QueryEmbedder
from app.query.formatter import (
    create_weaviate_filter,
    execute_search,
    execute_weighted_search,
)
from app.query import query_expander
from app.storage.connections import get_client


def main():
    print("--- Property Search Pipeline Test ---")
    user_input = input("Enter your search query: ")

    try:
        # Query expansion
        print("\nExpanding the query...")
        new_query = query_expander.get_query_expansion(user_input)
        expaned_query = new_query["expanded_query"]

        print(f"Expanded Query: {expaned_query}")

        # Get weights
        print("\nExtracted Weights:")
        weights = new_query["scaled_weights"]
        print(json.dumps(weights, indent=4))

        # 1. Extract structured data using the LLM chain
        print("\n[1/3] Extracting structured data...")
        result_segment = chain.invoke({"input": expaned_query})

        # 2. Generate vector embedding for the description
        print("[2/3] Generating vector embedding...")
        embedder = QueryEmbedder()
        query_vector = embedder.get_vector(result_segment.description)

        # 3. Format the Weaviate filters
        print("[3/3] Formatting Weaviate parameters...")
        wv_filter = create_weaviate_filter(result_segment)

        # Print the Final Payload Ready for Weaviate
        print("\n" + "=" * 50)
        print("READY FOR WEAVIATE HYBRID SEARCH")
        print("=" * 50)

        # Print Keyword portion
        print(f"User's Query: '{user_input}'")

        print(f"Expanded Query: '{expaned_query}'")

        # Print Vector portion (showing first 5 dims for brevity)
        vector_preview = query_vector[:5] if query_vector else []
        print(f"Vector (Dim: {len(query_vector)}): {vector_preview}...")

        # Print Filter portion
        # Note: Weaviate Filter objects have a specific internal structure
        print(f"Applied Filters: {wv_filter if wv_filter else 'None'}")

        print("\nFull Extracted Object (JSON):")
        print(json.dumps(result_segment.model_dump(), indent=4))

        # 4. Execute the search
        print("\n[4/4] Executing search on Weaviate...")
        with get_client() as client:
            # results = execute_weighted_search(
            #     expaned_query, query_vector, weights, client
            # )
            results = execute_search(user_input, query_vector, result_segment, client)

        # Print results
        print("\n" + "=" * 50)
        print("SEARCH RESULTS")
        print("=" * 50)
        if results:
            for i, obj in enumerate(results, 1):
                print(f"\nResult {i}:")
                print(f"  Title: {obj.properties.get('title', 'N/A')}")
                print(f"  Location: {obj.properties.get('location', 'N/A')}")
                print(f"  Price (LKR): {obj.properties.get('price_lkr', 'N/A')}")
                print(f"  Bedrooms: {obj.properties.get('bedrooms', 'N/A')}")
                print(f"  Bathrooms: {obj.properties.get('bathrooms', 'N/A')}")
                print(f"  Property Type: {obj.properties.get('property_type', 'N/A')}")
        else:
            print("No results found.")

        print("=" * 50)

    except Exception as e:

        print(f"ERROR in pipeline: {e}")


if __name__ == "__main__":
    main()
