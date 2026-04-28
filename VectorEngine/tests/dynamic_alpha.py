# The keys as they actually appear in processed entities
ENTITY_KEYS = [
    "property_type",
    "contract_type",
    "location",
    "no_of_bedrooms",
    "no_of_bathrooms",
    "price_min",  # price is always stored as price_min/max after post-processing
    "price_max",
    "land_size",
]

# F1 mapped to the actual entity keys
SLOT_F1 = {
    "property_type": 0.9521,
    "contract_type": 0.9463,
    "location": 0.9313,
    "no_of_bedrooms": 0.9630,
    "no_of_bathrooms": 0.9787,
    "price_min": 0.8898,
    "price_max": 0.8898,
    "land_size": 0.9346,
}


def _price_filled(entities: dict) -> bool:
    return (
        entities.get("price_min") is not None or entities.get("price_max") is not None
    )


def compute_alpha_from_entities(user_query: str, entities: dict) -> float:

    # ── 1. Slot-to-Residue Ratio ───────────────────────────────────
    STOP_WORDS = {
        "in",
        "at",
        "near",
        "with",
        "for",
        "the",
        "and",
        "of",
        "a",
        "an",
        "to",
        "on",
        "by",
        "from",
        "is",
        "are",
        "that",
        "which",
        "this",
        "has",
        "have",
        "want",
        "looking",
        "need",
        "show",
        "find",
        "get",
        "i",
        "me",
        "my",
        "any",
        "some",
        "please",
        "good",
        "nice",
        "great",
        "best",
        "around",
    }

    query_tokens = user_query.lower().split()
    meaningful_tokens = [t for t in query_tokens if t not in STOP_WORDS]

    # Collect all words that appear in any entity value
    slot_words = set()
    for key, val in entities.items():
        if val is None:
            continue
        for word in str(val).lower().split():
            slot_words.add(word)

    slot_token_count = sum(1 for t in meaningful_tokens if t in slot_words)
    slot_ratio = slot_token_count / len(meaningful_tokens)

    # ── 2. Slot Confidence (F1-weighted) ──────────────────────────
    # Treat price_min + price_max as a single slot
    SLOT_F1 = {
        "property_type": 0.9521,
        "contract_type": 0.9463,
        "location": 0.9313,
        "no_of_bedrooms": 0.9630,
        "no_of_bathrooms": 0.9787,
        "price": 0.8898,  # unified price slot
        "land_size": 0.9346,
    }
    F1_TOTAL = sum(SLOT_F1.values())  # 6.4958

    filled_f1 = 0.0
    for slot, f1 in SLOT_F1.items():
        if slot == "price":
            if _price_filled(entities):
                filled_f1 += f1
        elif entities.get(slot) is not None:
            filled_f1 += f1

    slot_conf = filled_f1 / F1_TOTAL

    # ── 3. Structuredness → Alpha ──────────────────────────────────
    structuredness = (0.5 * slot_ratio) + (0.5 * slot_conf)
    # structuredness = slot_ratio
    alpha = round(max(0.1, min(0.9, 1.0 - structuredness)), 4)

    return alpha
