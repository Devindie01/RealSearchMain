

#function to calculateslot coverage ratio = (number of slots with at least 1 value) / (total number of slots)
#total slots = 7 (property_type, contract_type, location, no_of_bedrooms, no_of_bathrooms, price, land_size)

TOTAL_SLOTS = [
    "property_type",
    "contract_type",
    "location",
    "no_of_bedrooms",
    "no_of_bathrooms",
    "price",
    "land_size"
]


def calculate_slot_coverage(raw_entities: dict) -> float:
    filled = 0

    for slot in TOTAL_SLOTS:
        if slot in raw_entities and len(raw_entities[slot]) > 0:
            filled += 1

    return filled / len(TOTAL_SLOTS)


#function to calculate slot confidence score = avg(confidence of all slot that have at least 1 value)
#confidence scores for each slot (SLOT_F1 = {"property_type": 0.9521,"contract_type": 0.9463,"location": 0.9313,"no_of_bedrooms": 0.9630,"price": 0.8898,"land_size": 0.9346,"no_of_bathrooms": 0.9787,})

SLOT_F1 = {
    "property_type": 0.9521,
    "contract_type": 0.9463,
    "location": 0.9313,
    "no_of_bedrooms": 0.9630,
    "price": 0.8898,
    "land_size": 0.9346,
    "no_of_bathrooms": 0.9787
}

def calculate_slot_confidence(raw_entities: dict) -> float:
    scores = []

    for slot, values in raw_entities.items():
        if slot in SLOT_F1 and len(values) > 0:
            scores.append(SLOT_F1[slot])

    if not scores:
        return 0.0

    return sum(scores) / len(scores)


#function to calculate non_slot_ratio = (number of tokens not part of any slot) / (total number of tokens in the query)

import spacy

nlp = spacy.load("en_core_web_sm")


def calculate_non_slot_ratio(query: str, raw_entities: dict) -> float:
    doc = nlp(query)

    total_tokens = len([t for t in doc if not t.is_punct])

    slot_tokens = set()

    for values in raw_entities.values():
        for v in values:
            for token in v.split():
                slot_tokens.add(token.lower())

    non_slot_tokens = 0

    for token in doc:
        if not token.is_punct and token.text.lower() not in slot_tokens:
            non_slot_tokens += 1

    if total_tokens == 0:
        return 0.0

    return non_slot_tokens / total_tokens


#functions to calcualte penalty for having multiple values for a single slot (e.g. "location: Colombo, Kandy" or "property_type: house or apartment")
# num_locations and num_property_types. if entity list has several values which has location tag or property_type tag, we apply a penalty to the final score. The penalty can be calculated as 0.1 for each additional value beyond the first one. For example, if there are 3 locations mentioned, the penalty would be 0.2 (0.1 for the second location and 0.1 for the third location). This encourages the model to prefer queries that are more specific and have fewer values for each slot.

def num_locations(raw_entities: dict) -> int:
    return len(raw_entities.get("location", []))

def num_property_types(entities: dict) -> int:
    return len(entities.get("property_type", []))

def build_features(query: str, entities: dict):

    return [
        calculate_slot_coverage(entities),
        calculate_slot_confidence(entities),
        calculate_non_slot_ratio(query, entities),
        num_locations(entities),
        num_property_types(entities)
    ]