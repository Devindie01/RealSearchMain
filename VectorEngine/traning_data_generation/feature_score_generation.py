TOTAL_SLOTS = [
    "property_type",
    "contract_type",
    "location",
    "no_of_bedrooms",
    "no_of_bathrooms",
    "price",
    "land_size",
]


def _has_value(val) -> bool:
    """Return True if a slot value is non-empty, regardless of type."""
    if val is None:
        return False
    if isinstance(val, (list, str)):
        return len(val) > 0
    return True  # int, float, etc. — presence itself counts


def _as_list(val) -> list:
    """Coerce any slot value to a list for uniform iteration."""
    if val is None:
        return []
    if isinstance(val, list):
        return val
    return [val]  # wrap scalar (int, str) in a list


def calculate_slot_coverage(raw_entities: dict) -> float:
    filled = sum(1 for slot in TOTAL_SLOTS if _has_value(raw_entities.get(slot)))
    return filled / len(TOTAL_SLOTS)


SLOT_F1 = {
    "property_type": 0.9521,
    "contract_type": 0.9463,
    "location": 0.9313,
    "no_of_bedrooms": 0.9630,
    "price": 0.8898,
    "land_size": 0.9346,
    "no_of_bathrooms": 0.9787,
}


def calculate_slot_confidence(raw_entities: dict) -> float:
    scores = [
        SLOT_F1[slot]
        for slot, val in raw_entities.items()
        if slot in SLOT_F1 and _has_value(val)
    ]
    return sum(scores) / len(scores) if scores else 0.0


import spacy

nlp = spacy.load("en_core_web_sm")


def _has_value(val) -> bool:
    if val is None:
        return False
    if isinstance(val, list):
        return len(val) > 0
    if isinstance(val, str):
        return len(val.strip()) > 0
    return True


def calculate_non_slot_ratio(query: str, raw_entities: dict) -> float:
    doc = nlp(query)
    total_tokens = len([t for t in doc if not t.is_punct])
    if total_tokens == 0:
        return 0.0

    slot_tokens = set()
    for key, val in raw_entities.items():
        # Ensure we iterate through lists (like locations) and single values correctly
        items = val if isinstance(val, list) else [val]
        for item in items:
            if item:
                for word in str(item).split():
                    slot_tokens.add(word.lower())

    non_slot_tokens = sum(
        1
        for token in doc
        if not token.is_punct and token.text.lower() not in slot_tokens
    )
    return non_slot_tokens / total_tokens


def num_locations(raw_entities: dict) -> int:
    return len(_as_list(raw_entities.get("location", [])))


def num_property_types(entities: dict) -> int:
    return len(_as_list(entities.get("property_type", [])))


def build_features(query: str, entities: dict):
    return [
        calculate_slot_coverage(entities),
        calculate_slot_confidence(entities),
        calculate_non_slot_ratio(query, entities),
        num_locations(entities),
        num_property_types(entities),
    ]
