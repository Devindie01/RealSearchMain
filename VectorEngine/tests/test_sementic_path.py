import sys
from pathlib import Path

# Ensure the project root (VectorEngine) is on sys.path so the `app` package
# can be imported when running this test directly (e.g. `python tests/...`).
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.query.query_expanision.classifer import (
    queryclassifier,
    map_entities_to_query_segment,
)
from app.query.query_expanision.semantic_query_handler import get_alpha_from_srr
from app.query.query_expanision.ambiguous_query_handler import (
    expand_and_bound_ambiguous_query,
)
from app.query.formatter import create_weaviate_filter
from app.query.executor.query_executor import QueryEmbedder, get_chain
from app.storage.connections import get_client

# Initialize the chain
chain = get_chain()


def run_pipeline_test(user_query, client):
    print(f"\n{'='*60}\nQUERY: {user_query}")

    # Step A: NLP Classification
    classification = queryclassifier(user_query)
    alpha = get_alpha_from_srr(classification)

    print(
        f"Type: {classification['type']} | SRR: {classification['SRR']:.2f} | Alpha: {alpha}"
    )

    if classification["type"] == "Semantic":

        entities = classification["entities"]
        leftover = classification["leftover_text"]

        result_segment = map_entities_to_query_segment(user_query, entities, leftover)

        # Step C: Vectorization
        embedder = QueryEmbedder()
        query_vector = embedder.get_vector(user_query)

        # Step D: Filter Construction
        wv_filter = create_weaviate_filter(result_segment)

        # Step E: Weaviate Hybrid Search
        properties = client.collections.get("RealSearch")

        results = properties.query.hybrid(
            query=user_query,  # Keyword part
            vector=query_vector,  # Vector part
            filters=wv_filter,  # Hard metadata filters
            alpha=alpha,  # Dynamically calculated weight
            limit=10,
        )
        # Print Results
        if results.objects:
            for i, obj in enumerate(results.objects, 1):
                p = obj.properties
                print(f" [{i}] {p.get('title')} - {p.get('priceLkr')} LKR")
        else:
            print(" No results found.")

    elif classification["type"] == "Ambiguous":
        predicted_queries = expand_and_bound_ambiguous_query(user_query)
        print(f"Predicted Queries: {predicted_queries}")
        all_properties = []
        for i, pq in enumerate(predicted_queries, 1):
            embedder = QueryEmbedder()
            query_vector = embedder.get_vector(pq)
            properties = client.collections.get("RealSearch")

            results = properties.query.hybrid(
                query=user_query,  # Keyword part
                vector=query_vector,  # Vector part
                alpha=1,  # Dynamically calculated weight
                limit=10,
            )
            all_properties.append(results.objects)

        if all_properties:
            for i, obj_list in enumerate(all_properties, 1):
                for j, obj in enumerate(obj_list, 1):
                    p = obj.properties
                    print(f" [{i}.{j}] {p.get('title')} - {p.get('priceLkr')} LKR")

    else:
        print("Non-semantic query detected. Skipping LLM extraction and vectorization.")


# --- 3. Execution ---

# if __name__ == "__main__":
queries = [
    "3 bedroom house kandy"
    # "20 perch land in Negombo near the beach for sale",
    # "house near Colombo with garden",
    # "calm place for retirement",
    # "apartment in Colombo with sea view for rent",
    # "land for sale in Colombo with good access to public transport",
    # "villa in Galle with pool and sea view for sale",
    # "affordable house in Kandy with 3 bedrooms and garden for rent",
]

with get_client() as client:
    for q in queries:
        try:
            run_pipeline_test(q, client)
        except Exception as e:
            print(f"Error processing '{q}': {e}")
