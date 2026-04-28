from collections import defaultdict

import spacy
import torch
import numpy as np
import re

from app.query.query_expanision.post_processing import (
    extract_number,
    extract_price_details,
    normalize_count,
)
from app.query.query_object import QuerySegment


# Load your model
# nlp = spacy.load(r"D:\FYP\RealSearch\VectorEngine\models\model-best")
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
nlp = spacy.load(os.path.join(BASE_DIR, "models", "model-best"))
JUNK_WORDS = ["in", "at", "near", "with", "for", "the", "and", "of"]


def extract_entities_from_user_query(user_query):
    doc = nlp(user_query)

    # ✅ Step 1: Collect multiple values per slotError processing query
    raw_entities = defaultdict(list)

    for ent in doc.ents:
        words = ent.text.split()

        # Clean trailing junk words
        if words[-1].lower() in JUNK_WORDS:
            clean_text = " ".join(words[:-1])
        else:
            clean_text = ent.text

        raw_entities[ent.label_].append(clean_text)

    # ✅ Step 2: Post-processing
    processed = {}

    # Property types (keep all)
    if "property_type" in raw_entities:
        processed["property_type"] = list(set(raw_entities["property_type"]))

    # Locations (keep all)
    if "location" in raw_entities:
        processed["location"] = list(set(raw_entities["location"]))

    # Contract type (take first)
    if "contract_type" in raw_entities:
        processed["contract_type"] = raw_entities["contract_type"][0]

    # Bedrooms
    if "no_bedrooms" in raw_entities:
        processed["no_of_bedrooms"] = normalize_count(raw_entities["no_bedrooms"][0])

    # Bathrooms
    if "no_bathrooms" in raw_entities:
        processed["no_of_bathrooms"] = normalize_count(raw_entities["no_bathrooms"][0])

    # Land size
    if "land_size" in raw_entities:
        processed["land_size"] = extract_number(raw_entities["land_size"][0])

    # Price
    if "price" in raw_entities:
        price_min, price_max, currency, period = extract_price_details(
            raw_entities["price"][0]
        )

        processed["price_min"] = price_min
        processed["price_max"] = price_max
        processed["price_unit"] = currency

        if processed.get("contract_type") in ["rent", "lease"]:
            processed["price_period"] = period

    return {"entities": processed, "raw_entities": raw_entities}  # optional debug


# def queryclassifier(features):
#     slot_coverage, slot_conf, non_slot_ratio, num_loc, num_prop = features

#     # semantic conditions
#     if slot_coverage == 0:
#         return "Ambiguous"

#     # otherwise ambiguous
#     return "Semantic"


def queryclassifier(entities):
    # res = extract_entities_from_user_query(user_query)
    # entities = res["entities"]

    if len(entities) == 0:
        return "Ambiguous"
    else:
        return "Semantic"


# def map_entities_to_query_segment(
#     user_query: str, entities: dict, leftover_text: str
# ) -> QuerySegment:
#     # 1. Initialize data with leftover text
#     data = {
#         "description": leftover_text if leftover_text else user_query,
#         "property_type": None,
#         "contract_type": None,
#         "price": None,
#         "location": None,
#         "no_of_bedrooms": None,
#         "no_of_bathrooms": None,
#         "land_size": None,
#     }

#     # 2. Map spaCy labels to Pydantic fields
#     label_map = {
#         "property_type": "property_type",
#         "contract_type": "contract_type",
#         "location": "location",
#         "price": "price",
#         "no_bedrooms": "no_of_bedrooms",
#         "no_bathrooms": "no_of_bathrooms",
#         "land_size": "land_size",
#     }

#     # 3. Iterate through the dictionary returned by your spaCy function
#     # 'label' is the key (e.g., 'location'), 'value' is the text (e.g., 'Negombo')
#     for label, value in entities.items():
#         if label in label_map:
#             data[label_map[label]] = value

#     return QuerySegment(**data)


# def map_entities_to_query_segment(
#     user_query: str, entities: dict, leftover_text: str
# ) -> QuerySegment:
#     data = {
#         "description": leftover_text if leftover_text else user_query,
#         "property_type": None,
#         "contract_type": None,
#         "price": None,
#         "location": None,
#         "no_of_bedrooms": None,
#         "no_of_bathrooms": None,
#         "land_size": None,
#     }

#     label_map = {
#         "property_type": "property_type",
#         "contract_type": "contract_type",
#         "location": "location",
#         "price": "price",
#         "no_bedrooms": "no_of_bedrooms",
#         "no_bathrooms": "no_of_bathrooms",
#         "land_size": "land_size",
#     }

#     for label, value in entities.items():
#         if label in label_map:
#             field_name = label_map[label]
#             # --- NEW LOGIC START ---
#             # If the field is a count or size, extract only the number
#             if field_name in [
#                 "no_of_bedrooms",
#                 "no_of_bathrooms",
#                 "land_size",
#                 "price",
#             ]:
#                 data[field_name] = extract_number(value)
#             else:
#                 data[field_name] = value
#             # --- NEW LOGIC END ---

#     return QuerySegment(**data)


# --- Test ---
# q1 = "Looking for a 3 bedroom apartment near Colombo with a sea view"
# q2 = "house near Colombo with garden"
# q3 = "apartment in Colombo with sea view for rent"
# q4 = "land for sale in Colombo with good access to public transport"
# q5 = "calm place for retirement"

# for q in [q1]:
#     # 1. Get the raw extraction first
#     extraction = extract_entities_and_leftovers_smart(q)

#     # 2. Get the classification category
#     classification = queryclassifier(q)

#     print(f"Query: {q}")
#     print(f"Classification: {classification}")
#     print(f"Entities: {extraction['entities']}")
#     print(f"Leftover: {extraction['leftover_text']}\n")
