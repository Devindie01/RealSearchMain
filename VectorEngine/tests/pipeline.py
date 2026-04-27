import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from traning_data_generation.feature_score_generation import build_features
from app.query.query_expanision.query_normalizer import clean_query
from app.query.query_expanision.post_processing import build_query_segments
from app.query.query_expanision.classifer import (
    extract_entities_from_user_query,
    queryclassifier,
)
from app.query.query_expanision.semantic_query_handler import get_alpha_from_entities
from app.query.query_expanision.ambiguous_query_handler import (
    expand_and_bound_ambiguous_query,
)
from app.query.formatter import create_weaviate_filter

# from app.query.executor.query_executor import QueryEmbedder


def _to_int(val):
    """Safely convert a property ID to int for consistent comparison."""
    try:
        return int(val)
    except (TypeError, ValueError):
        return val


def run_pipeline_test(user_query, client):
    print(f"\n{'='*60}\nQUERY: {user_query}")

    user_query = clean_query(user_query)

    res = extract_entities_from_user_query(user_query)
    entities = res["entities"]
    print(f"Extracted Entities: {entities}")

    features = build_features(
        user_query, entities
    )  # ✅ no fallback — real errors will surface
    print(f"Extracted Features: {features}")

    alpha = compute_alpha(features)
    print(f"Computed Alpha: {alpha}")

    type_label = queryclassifier(features)
    classification = {"type": type_label}

    print(f"Type: {classification['type']} | Alpha: {alpha:.3f}")

    if classification["type"] == "Semantic":

        properties = client.collections.get("RealSearchPropData")

        results = properties.query.hybrid(
            query=user_query,
            # vector=query_vector,
            # filters=wv_filter,
            alpha=alpha,
            limit=10,
        )

        retrieved_ids = []
        if results.objects:
            for i, obj in enumerate(results.objects, 1):
                p = obj.properties
                pid = _to_int(p.get("propertyId"))
                retrieved_ids.append(pid)
                print(f" [{i}] {p.get('title')})")
        else:
            print(" No results found.")

        return retrieved_ids

    elif classification["type"] == "Ambiguous":

        predicted_queries = expand_and_bound_ambiguous_query(user_query)
        print(f"Predicted Queries: {predicted_queries}")

        seen = set()
        retrieved_ids = []

        properties = client.collections.get("RealSearchPropData")

        for i, pq in enumerate(predicted_queries, 1):

            pq = clean_query(pq)

            res = extract_entities_from_user_query(pq)
            entities = res["entities"]

            features = build_features(pq, entities)
            alpha = compute_alpha(features)
            qtype = queryclassifier(features)

            print(f"\n[Expansion {i}] Type: {qtype} | Alpha: {alpha:.3f}")

            # if becomes semantic → use semantic retrieval
            if qtype == "Semantic":
                results = properties.query.hybrid(
                    query=pq,
                    alpha=alpha,
                    limit=10,
                )

            else:
                # fallback hybrid
                results = properties.query.hybrid(
                    query=pq,
                    alpha=1,
                    limit=10,
                )

            if results.objects:
                for obj in results.objects:
                    pid = _to_int(obj.properties.get("propertyId"))

                    if pid not in seen:
                        seen.add(pid)
                        retrieved_ids.append(pid)

                        print(f"  [{i}] {obj.properties.get('title')}")

        return retrieved_ids[:10]

    else:
        print("Non-semantic query detected. Skipping.")
        return []


def compute_alpha(features):
    slot_coverage, slot_conf, non_slot_ratio, num_loc, num_prop = features

    # num_loc = min(num_loc / 3, 1.0)
    num_prop = min(num_prop / 3, 1.0)

    alpha = (
        +0.4 * non_slot_ratio
        # + 0.2 * num_loc
        + 0.2 * num_prop
        - 0.35 * slot_coverage
        - 0.35 * slot_conf
    )

    alpha = 0.5 + alpha
    alpha = max(0.1, min(0.9, alpha))

    return alpha
