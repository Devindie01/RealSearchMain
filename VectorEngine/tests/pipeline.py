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


from weaviate.classes.query import Filter, GeoCoordinate  # GeoCoordinate for the geo filter

GEO_RADIUS_KM = 25.0


def fetch_location_coordinates(location: str) -> tuple[float, float] | None:
    """
    Resolve a location name to (lat, lon) using the OpenStreetMap Nominatim API.
    """
    if not location:
        return None

    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": location.strip(), "format": "json", "limit": 1}
    headers = {"User-Agent": "RealSearch/1.0 (property-search-app)"}

    try:
        import httpx
        response = httpx.get(url, params=params, headers=headers, timeout=5.0)
        response.raise_for_status()
        data = response.json()
        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            print(f"  🌍 Nominatim resolved {location!r} → ({lat}, {lon})")
            return (lat, lon)
        print(f"  ⚠️  Nominatim returned no results for: {location!r}")
    except Exception as e:
        print(f"  ⚠️  fetch_location_coordinates failed: {e}")

    return None


def build_filters(price_min, price_max, bedrooms, bathrooms,
                  property_type=None, contract_type=None,
                  location=None, client=None):
    filters = []

    # ── Price (±10% margin) ───────────────────────────────────────────────────
    if price_min is not None and price_max is not None:
        filters.append(
            Filter.by_property("priceLKR").greater_or_equal(price_min * 0.90)
            & Filter.by_property("priceLKR").less_or_equal(price_max * 1.10)
        )
    elif price_min is not None:
        filters.append(Filter.by_property("priceLKR").greater_or_equal(price_min * 0.90))
    elif price_max is not None:
        filters.append(Filter.by_property("priceLKR").less_or_equal(price_max * 1.10))

    # ── Bedrooms (±2) ─────────────────────────────────────────────────────────
    if bedrooms is not None:
        filters.append(
            Filter.by_property("bedrooms").greater_or_equal(max(0, bedrooms - 2))
            & Filter.by_property("bedrooms").less_or_equal(bedrooms + 2)
        )

    # ── Bathrooms (±2) ────────────────────────────────────────────────────────
    if bathrooms is not None:
        filters.append(
            Filter.by_property("bathrooms").greater_or_equal(max(0, bathrooms - 2))
            & Filter.by_property("bathrooms").less_or_equal(bathrooms + 2)
        )

    # ── Property type (exact) ─────────────────────────────────────────────────
    if property_type:
        filters.append(Filter.by_property("propertyType").equal(property_type))

    # ── Contract type (exact) ─────────────────────────────────────────────────
    if contract_type:
        filters.append(Filter.by_property("contractType").equal(contract_type))

    # ── Geo filter (native Weaviate GeoCoordinates) ───────────────────────────
    if location:
        print("sgsjrbgsub")
        coords = fetch_location_coordinates(location)
        if coords:
            lat, lon = coords
            print(f"  📍 Geo filter: {location!r} → ({lat:.4f}, {lon:.4f}) ±{GEO_RADIUS_KM} km")
            filters.append(
                Filter.by_property("geoLocation").within_geo_range(
                    coordinate=GeoCoordinate(latitude=lat, longitude=lon),
                    distance=GEO_RADIUS_KM * 1000,  # Weaviate expects metres
                )
            )
        else:
            print(f"  ⚠️  Could not resolve coordinates for: {location!r}")

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
    location=None,           # ← add this
    property_type=None,      # ← add this
    contract_type=None,
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
    property_type = entities.get("property_type")[0] if entities.get("property_type") else None
    contract_type = entities.get("contract_type") if entities.get("contract_type") else None
    location = entities.get("location")[0] if entities.get("location") else None
    bedrooms = entities.get("no_of_bedrooms") if entities.get("no_of_bedrooms") else None
    bathrooms = entities.get("no_of_bathrooms") if entities.get("no_of_bathrooms") else None
    area = entities.get("area")[0] if entities.get("area") else None
    
    print("location:", location)

    wv_filter = build_filters(price_min, price_max, bedrooms=bedrooms, bathrooms=bathrooms, location=location, property_type=property_type, contract_type=contract_type)

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
