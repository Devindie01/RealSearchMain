# from weaviate.classes.query import Filter
# import sys
# from pathlib import Path
# from weaviate.classes.query import Filter
# import random
# ROOT = Path(__file__).resolve().parents[1]
# sys.path.insert(0, str(ROOT))

# from traning_data_generation.feature_score_generation import build_features
# from app.query.query_expanision.query_normalizer import clean_query
# from app.query.query_expanision.post_processing import build_query_segments
# from app.query.query_expanision.classifer import (
#     extract_entities_from_user_query,
#     queryclassifier,
# )
# from app.query.query_expanision.semantic_query_handler import get_alpha_from_entities
# from app.query.query_expanision.ambiguous_query_handler import (
#     expand_and_bound_ambiguous_query,
# )
# from tests.dynamic_alpha import compute_alpha_from_entities
# from app.query.formatter import create_weaviate_filter

# # from app.query.executor.query_executor import QueryEmbedder


# def _to_int(val):
#     """Safely convert a property ID to int for consistent comparison."""
#     try:
#         return int(val)
#     except (TypeError, ValueError):
#         return val


# def run_pipeline_test(
#     user_query,
#     price_min,
#     price_max,
#     bedrooms,
#     bathrooms,
#     area,
#     client,
# ):
#     print(f"\n{'='*60}\nQUERY: {user_query}")

#     user_query = clean_query(user_query)

#     res = extract_entities_from_user_query(user_query)
#     raw_entities = res["raw_entities"]
#     print(f"Raw Extracted Entities: {raw_entities}")
#     entities = res["entities"]
#     print(f"Extracted Entities: {entities}")

#     # features = build_features(
#     #     user_query, entities
#     # )  # ✅ no fallback — real errors will surface
#     # print(f"Extracted Features: {features}")

#     type_label = queryclassifier(entities)

#     classification = {"type": type_label}

#     print(f"Type: {classification['type']}")

#     if classification["type"] == "Semantic":

#         alpha = compute_alpha_from_entities(user_query, entities)
#         print(f"Computed Alpha: {alpha}")

#         # wv_filter = create_weaviate_filter(build_query_segments(entities))

#         properties = client.collections.get("RealSearchPropDataf")

#         results = properties.query.hybrid(
#             query=user_query,
#             # # vector=query_vector,
#             # filters=(Filter.by_property("bedrooms").equal("10")),
#             #if parameters are present, add hard filters based on that
#             if price_min and price_max is not None:
#                 filters=Filter.by_property("price").between(price_min, price_max),
#             if price_min not None:
#                 filters=Filter.by_property("price").greater_than(price_min),
#             if price_max not None:
#                 filters=Filter.by_property("price").less_than(price_max),
#             if bedrooms is not None:
#                 filters=Filter.by_property("bedrooms").between(bedrooms-1, bedrooms+1),
#             if bathrooms is not None:
#                 filters=Filter.by_property("bathrooms").between(bathrooms-1, bathrooms+1),
#             alpha=alpha,
#             limit=10,
#         )

#     #     results = properties.query.hybrid(
#     #         query=user_query,  # soft filter injected here
#     #         alpha=0.5,
#     #         target_vector="default",                       # optional explicit vector
#     #         query_properties=["description", "bedroom_text"],  # BM25 scope
#     #         limit=10,
#     #         return_metadata=client.query.MetadataQuery(score=True)
#     # #    )

#     #     for obj in results.objects:
#     #         print(obj.properties["title"], obj.properties["bedroom_count"], obj.metadata.score)

#         retrieved_ids = []
#         if results.objects:
#             for i, obj in enumerate(results.objects, 1):
#                 p = obj.properties
#                 pid = _to_int(p.get("propertyId"))
#                 retrieved_ids.append(pid)
#                 print(f" [{i}] {p.get('title')})")
#         else:
#             print(" No results found.")

#         return retrieved_ids

#     # elif classification["type"] == "Ambiguous":
#     #     predicted_queries = expand_and_bound_ambiguous_query(user_query)
#     #     print(f"Predicted Queries: {predicted_queries}")
#     #     all_properties = []
#     #     for i, pq in enumerate(predicted_queries, 1):
#     #         properties = client.collections.get("RealSearchPropDataf")

#     #         results = properties.query.hybrid(
#     #             query=user_query,  # Keyword part
#     #             # vector=query_vector,  # Vector part
#     #             alpha=1,  # Dynamically calculated weight
#     #             limit=10,
#     #         )
#     #         all_properties.append(results.objects)

#     #     if all_properties:
#     #         for i, obj_list in enumerate(all_properties, 1):
#     #             for j, obj in enumerate(obj_list, 1):
#     #                 p = obj.properties
#     #                 print(f" [{i}.{j}] {p.get('title')}")
#     elif classification["type"] == "Ambiguous":
#         predicted_queries = expand_and_bound_ambiguous_query(user_query)
#         print(f"Predicted Queries: {predicted_queries}")

#         all_properties = []

#         for i, pq in enumerate(predicted_queries, 1):
#             properties = client.collections.get("RealSearchPropDataf")

#             results = properties.query.hybrid(
#                 query=pq,  # ✅ IMPORTANT: use pq, not user_query
#                 alpha=1,
#                 limit=10,
#             )

#             if results.objects:
#                 all_properties.extend(results.objects)

#         retrieved_ids = []
#         seen = set()

#         if all_properties:
#             for i, obj in enumerate(all_properties, 1):
#                 p = obj.properties
#                 pid = _to_int(p.get("propertyId"))

#                 print(f" [{i}] {p.get('title')}")

#                 if pid is not None and pid not in seen:
#                     seen.add(pid)
#                     retrieved_ids.append(pid)

#         final_ids = random.sample(retrieved_ids, min(10, len(retrieved_ids)))
#         # ✅ FINAL RETURN (this was missing)
#         return final_ids if final_ids else []

#         # # ✅ FINAL RETURN (this was missing)
#         # return retrieved_ids[:10] if retrieved_ids else []

#     else:
#         print("Non-semantic query detected. Skipping LLM extraction and vectorization.")


# def compute_alpha(features):
#     slot_coverage, slot_conf, non_slot_ratio, num_loc, num_prop = features

#     # num_loc = min(num_loc / 3, 1.0)
#     num_prop = min(num_prop / 3, 1.0)

#     alpha = (
#         +0.4 * non_slot_ratio
#         # + 0.2 * num_loc
#         + 0.2 * num_prop
#         - 0.35 * slot_coverage
#         - 0.35 * slot_conf
#     )

#     alpha = 0.5 + alpha
#     alpha = max(0.1, min(0.9, alpha))

#     return alpha


from weaviate.classes.query import Filter
import sys
from pathlib import Path
from weaviate.classes.query import Filter
import random

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
from tests.dynamic_alpha import compute_alpha_from_entities
from app.query.formatter import create_weaviate_filter


def _to_int(val):
    """Safely convert a property ID to int for consistent comparison."""
    try:
        return int(val)
    except (TypeError, ValueError):
        return val


def build_filters(price_min, price_max, bedrooms, bathrooms):
    """Build a combined Weaviate filter. Returns None if no params provided."""
    filters = []

    if price_min is not None and price_max is not None:
        filters.append(
            Filter.by_property("price").greater_or_equal(price_min)
            & Filter.by_property("price").less_or_equal(price_max)
        )
    elif price_min is not None:
        filters.append(Filter.by_property("priceLKR").greater_or_equal(price_min))
    elif price_max is not None:
        filters.append(Filter.by_property("priceLKR").less_or_equal(price_max))

    if bedrooms is not None:
        filters.append(
            Filter.by_property("bedrooms").greater_or_equal(bedrooms - 1)
            & Filter.by_property("bedrooms").less_or_equal(bedrooms + 1)
        )

    if bathrooms is not None:
        filters.append(
            Filter.by_property("bathrooms").greater_or_equal(bathrooms - 1)
            & Filter.by_property("bathrooms").less_or_equal(bathrooms + 1)
        )

    if not filters:
        return None

    combined = filters[0]
    for f in filters[1:]:
        combined = combined & f
    return combined


def run_pipeline_test(
    user_query,
    price_min,
    price_max,
    bedrooms,
    bathrooms,
    area,
    client,
    lambda_: float = 0.5,
):
    print(f"\n{'='*60}\nQUERY: {user_query}")

    user_query = clean_query(user_query)

    res = extract_entities_from_user_query(user_query)
    raw_entities = res["raw_entities"]
    print(f"Raw Extracted Entities: {raw_entities}")
    entities = res["entities"]
    print(f"Extracted Entities: {entities}")

    type_label = queryclassifier(entities)

    classification = {"type": type_label}

    print(f"Type: {classification['type']}")

    wv_filter = build_filters(price_min, price_max, bedrooms, bathrooms)

    if classification["type"] == "Semantic":

        alpha = compute_alpha_from_entities(user_query, entities, lambda_)
        print(f"Computed Alpha: {alpha}")

        properties = client.collections.get("FypCollection")

        query_kwargs = dict(query=user_query, alpha=alpha, limit=10)
        if wv_filter is not None:
            query_kwargs["filters"] = wv_filter

        results = properties.query.hybrid(**query_kwargs)

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

        all_properties = []

        for i, pq in enumerate(predicted_queries, 1):
            properties = client.collections.get("FypCollection")

            query_kwargs = dict(query=pq, alpha=1, limit=10)
            if wv_filter is not None:
                query_kwargs["filters"] = wv_filter

            results = properties.query.hybrid(**query_kwargs)

            if results.objects:
                all_properties.extend(results.objects)

        retrieved_ids = []
        seen = set()

        if all_properties:
            for i, obj in enumerate(all_properties, 1):
                p = obj.properties
                pid = _to_int(p.get("propertyId"))

                print(f" [{i}] {p.get('title')}")

                if pid is not None and pid not in seen:
                    seen.add(pid)
                    retrieved_ids.append(pid)

        final_ids = random.sample(retrieved_ids, min(10, len(retrieved_ids)))
        return final_ids if final_ids else []

    else:
        print("Non-semantic query detected. Skipping LLM extraction and vectorization.")


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
