import dspy
import os
from dotenv import load_dotenv

load_dotenv()

# Setup DSPy to use OpenRouter
lm = dspy.LM(
    model="openrouter/mistralai/mistral-large-2411",  # Or your preferred model
    api_key=os.getenv("OPENROUTER_API_KEY"),
    api_base="https://openrouter.ai/api/v1",
    max_tokens=500,
    # OpenRouter often requires these headers for free/certain models
    extra_headers={
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "RealSearch_FYP",
    },
)

dspy.configure(lm=lm)


class ExpandQuery(dspy.Signature):
    """Expand a property search query into semantic keywords and assign weights (0-1) to filters."""

    user_query = dspy.InputField(desc="The raw search query from the user")

    # We restrict the keys here to match your Weaviate 'query_properties'
    weights = dspy.OutputField(
        desc="Weights (0.0-1.0) for: location, price, contract_type, property_type, no_of_bedrooms, no_of_bathrooms, land_size, description"
    )
    expanded_query = dspy.OutputField(
        desc="The user query expanded with synonyms for better semantic matching"
    )

import re

def get_query_expansion(user_input: str):
    """
    Takes a raw user query and returns:
    1. The expanded semantic text
    2. A dictionary of scaled integer weights (1-10)
    """
    # 1. Run the DSPy prediction
    expander = dspy.ChainOfThought(ExpandQuery)
    prediction = expander(user_query=user_input)
    
    # 2. Extract weights using regex (handles "key:value" string formats)
    # This finds word:number patterns like 'location:0.9'
    raw_weights = prediction.weights
    parsed_weights = {}
    
    if isinstance(raw_weights, str):
        # Find all key:value pairs
        matches = re.findall(r"(\w+):([\d\.]+)", raw_weights)
        for key, value in matches:
            # Scale 0.0-1.0 to 1-10
            parsed_weights[key] = max(1, int(float(value) * 10))
    else:
        # If DSPy already returned a dict, just scale the values
        for key, value in raw_weights.items():
            parsed_weights[key] = max(1, int(float(value) * 10))

    return {
        "expanded_query": prediction.expanded_query,
        "scaled_weights": parsed_weights
    }


# # Example Usage
# expander = dspy.Predict(ExpandQuery)
# prediction = expander(user_query="Modern 2 bed flat in London with a balcony")

# print(f"Expanded Keywords: {prediction.expanded_query}")
# print(f"Weights: {prediction.weights}")
