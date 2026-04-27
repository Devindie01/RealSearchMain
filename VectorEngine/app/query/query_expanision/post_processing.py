import re
import spacy

from app.query.query_object import QuerySegment

WORD_TO_NUMBER = {
    "single": 1,
    "one": 1,
    "two": 2,
    "three": 3,
}


def extract_number(text):
    """Extracts a full number from text, handling commas."""
    if not text:
        return None

    # Remove commas (150,000 → 150000)
    cleaned = str(text).replace(",", "")

    match = re.search(r"\d+", cleaned)
    return int(match.group()) if match else None


def normalize_count(value: str):
    if not value:
        return None

    value = value.lower()

    # Try digit first
    num = extract_number(value)
    if num:
        return num

    # Try word mapping
    for word, number in WORD_TO_NUMBER.items():
        if word in value:
            return number

    return None


import re

import re


def extract_price_details(text: str):
    if not text:
        return None, None, None, None

    text = text.lower().replace(",", "")

    # ---------------------------
    # Currency detection
    # ---------------------------
    currency_match = re.search(r"(lkr|rs|rupees|usd)", text)
    currency = currency_match.group(1).upper() if currency_match else None

    if currency in ["RS", "RUPEES"]:
        currency = "LKR"

    # ---------------------------
    # Extract ALL numeric values
    # ---------------------------
    raw_numbers = re.findall(r"\d+(?:\.\d+)?", text)

    if not raw_numbers:
        return None, None, None, None

    numbers = [float(n) for n in raw_numbers]

    # ---------------------------
    # Multiplier detection
    # ---------------------------
    multiplier = 1

    if re.search(r"million|mn|mil", text):
        multiplier = 1_000_000
    elif re.search(r"lakh|lakhs", text):
        multiplier = 100_000
    elif re.search(r"crore|crores", text):
        multiplier = 10_000_000

    numbers = [n * multiplier for n in numbers]

    # ---------------------------
    # Assign min/max logic
    # ---------------------------
    if len(numbers) == 1:
        price_min = None
        price_max = int(numbers[0])
    else:
        price_min = int(min(numbers))
        price_max = int(max(numbers))

    # ---------------------------
    # Period detection (rent/lease)
    # ---------------------------
    period_match = re.search(r"per\s+(month|week|year|day)", text)
    period = period_match.group(1) if period_match else None

    return price_min, price_max, currency, period


def split_property_types(value: str):
    if not value:
        return [None]

    # Split by "or", ","
    types = re.split(r",|or", value.lower())
    return [t.strip() for t in types if t.strip()]


def build_query_segments(user_query, entities):
    # 'entities' here is the 'processed' dict from extract_entities_from_user_query
    data = {
        "description": user_query,
        "property_type": entities.get("property_type", []), # Use empty list, not [None]
        "contract_type": entities.get("contract_type"),     # Already a string or None
        "price_min": entities.get("price_min"),
        "price_max": entities.get("price_max"),
        "price_unit": entities.get("price_unit"),
        "price_period": entities.get("price_period"),
        "location": entities.get("location", []),           # Use empty list
        "no_of_bedrooms": entities.get("no_of_bedrooms"),
        "no_of_bathrooms": entities.get("no_of_bathrooms"),
        "land_size": entities.get("land_size"),
    }
    return QuerySegment(**data)

    # --- Normalize shared fields ---
    contract_type = entities.get("contract_type", [None])[0]

    bedrooms = normalize_count(entities.get("no_bedrooms", [None])[0])
    bathrooms = normalize_count(entities.get("no_bathrooms", [None])[0])

    price_min, price_max, currency, period = extract_price_details(
        entities.get("price", [None])[0]
    )

    # Locations → keep ALL
    locations = entities.get("location", [])

    # Property types → main splitter
    property_types = entities.get("property_type", [None])

    land_size = extract_number(entities.get("land_size", [None])[0])

    data = {
    "description": user_query,
    "property_type": property_types,
    "contract_type": contract_type,

    "price_min": price_min,
    "price_max": price_max,
    "price_unit": currency,
    "price_period": period,

    "location": locations,
    "no_of_bedrooms": bedrooms,
    "no_of_bathrooms": bathrooms,
    "land_size": land_size,
}

    return QuerySegment(**data)

