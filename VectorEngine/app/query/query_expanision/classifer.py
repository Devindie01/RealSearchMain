import spacy

from app.query.query_object import QuerySegment

# Load your model
nlp = spacy.load(r"D:\FYP\RealSearch\VectorEngine\models\Model")


def extract_entities_and_leftovers_smart(user_query):
    doc = nlp(user_query)

    # 1. Clean Entities (Fixing the "Colombo with" issue)
    # We strip trailing prepositions/connectors from the entity text
    junk_words = ["in", "at", "near", "with", "for", "the", "and", "of"]
    entities = {}
    for ent in doc.ents:
        words = ent.text.split()
        # If the last word of the entity is in our junk list, remove it
        if words[-1].lower() in junk_words:
            clean_text = " ".join(words[:-1])
        else:
            clean_text = ent.text
        entities[ent.label_] = clean_text

    # 2. Intelligent Leftover Filtering
    leftover_tokens = []

    for i, token in enumerate(doc):
        # Skip tokens that are part of a (now cleaned) entity
        if token.ent_type_ != "":
            # Check if this specific token was one we "trimmed" (like 'with' in 'Colombo with')
            # If the NER model tagged it but it's a junk word, we treat it as leftover
            if token.text.lower() not in junk_words:
                continue

        # Logic: If it's a preposition/determiner
        if token.text.lower() in junk_words:
            # Check neighbors: Is it next to an entity?
            has_entity_neighbor = False

            # Look left
            if i > 0 and doc[i - 1].ent_type_ != "":
                has_entity_neighbor = True
            # Look right
            if i < len(doc) - 1 and doc[i + 1].ent_type_ != "":
                has_entity_neighbor = True

            # If it's touching an entity, it's a "connector" -> Ignore it
            if has_entity_neighbor:
                continue

        leftover_tokens.append(token.text)

    return {"entities": entities, "leftover_text": " ".join(leftover_tokens).strip()}


def map_entities_to_query_segment(
    user_query: str, entities: dict, leftover_text: str
) -> QuerySegment:
    # 1. Initialize data with leftover text
    data = {
        "description": leftover_text if leftover_text else user_query,
        "property_type": None,
        "contract_type": None,
        "price": None,
        "location": None,
        "no_of_bedrooms": None,
        "no_of_bathrooms": None,
        "land_size": None,
    }

    # 2. Map spaCy labels to Pydantic fields
    label_map = {
        "property_type": "property_type",
        "contract_type": "contract_type",
        "location": "location",
        "price": "price",
        "no_bedrooms": "no_of_bedrooms",
        "no_bathrooms": "no_of_bathrooms",
        "land_size": "land_size",
    }

    # 3. Iterate through the dictionary returned by your spaCy function
    # 'label' is the key (e.g., 'location'), 'value' is the text (e.g., 'Negombo')
    for label, value in entities.items():
        if label in label_map:
            data[label_map[label]] = value

    return QuerySegment(**data)


def queryclassifier(user_query):
    res = extract_entities_and_leftovers_smart(user_query)
    entities = res["entities"]
    leftover = res["leftover_text"]

    if len(entities) == 0:
        res["type"] = "Ambiguous"
        res["SRR"] = 0
    else:
        if len(leftover) == 0:
            res["type"] = "Structured"
            res["SRR"] = float("inf")
        else:
            slotRatio = len(entities) / 7
            residualration = len(leftover) / len(user_query)
            res["SRR"] = (
                slotRatio / residualration if residualration > 0 else float("inf")
            )
            res["type"] = "Semantic"

    return res


# --- Test ---
q1 = "Looking for a 3 bedroom apartment near Colombo with a sea view"
# q2 = "house near Colombo with garden"
# q3 = "apartment in Colombo with sea view for rent"
# q4 = "land for sale in Colombo with good access to public transport"
# q5 = "calm place for retirement"

for q in [q1]:
    # 1. Get the raw extraction first
    extraction = extract_entities_and_leftovers_smart(q)

    # 2. Get the classification category
    classification = queryclassifier(q)

    print(f"Query: {q}")
    print(f"Classification: {classification}")
    print(f"Entities: {extraction['entities']}")
    print(f"Leftover: {extraction['leftover_text']}\n")
