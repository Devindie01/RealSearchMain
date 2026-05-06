"""
explainability.py
-----------------
Explainability engine for property recommendations.

Inputs:
    - user_query (str): The original natural language search query
    - property_id (str): ID of the retrieved property
    - property_description (str): Full property description as a plain string

Output:
    {
        "query": <original user query>,
        "property_id": <property id>,
        "explanation": <natural language explanation>
    }

Usage:
    from explainability import ExplainabilityEngine

    engine = ExplainabilityEngine()
    result = engine.explain(
        user_query="3 bedroom villa near airport under 50 million",
        property_id="PROP-1023",
        property_description="A 3-bedroom villa in Colombo listed for sale at LKR 47 million ..."
    )
"""

from langchain_openai import ChatOpenAI

# ---------------------------------------------------------------------------
# Configuration — hardcode your API key and model here
# ---------------------------------------------------------------------------

OPENROUTER_API_KEY = "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"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "openai/gpt-4o-mini"

# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """
You are a helpful real estate assistant that explains why a property matches a user's search.
Given the user's original search query and the property details, explain clearly and concisely
why this property was recommended. Focus on how the property aligns with what the user asked for,
and honestly note any aspects that may not be a perfect match.
Do not mention AI, embeddings, or vector search. Keep it friendly and easy to understand.

Give maximum 60 words explanation. Use simple language and avoid jargon. Be specific about which features of the property match the user's query (e.g., location, price, number of bedrooms) and also mention any key mismatches if relevant (e.g., "The user asked for a garden, but this property does not have one").
""".strip()

# ---------------------------------------------------------------------------
# Core engine
# ---------------------------------------------------------------------------

class ExplainabilityEngine:
    """
    Generates a natural language explanation for why a property was
    recommended for a given user query.
    """

    def __init__(
        self,
        api_key: str = OPENROUTER_API_KEY,
        base_url: str = OPENROUTER_BASE_URL,
        model_name: str = MODEL_NAME,
        temperature: float = 0.1,
    ):
        self._llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            base_url=base_url,
            api_key=api_key,
        )

    def explain(
        self,
        user_query: str,
        property_id: str,
        property_description: str,
    ) -> dict:
        """
        Generate an explanation for a recommended property.

        Args:
            user_query:            Original natural language query from the user.
            property_id:           Unique identifier of the retrieved property.
            property_description:  Full property description as a plain string.

        Returns:
            {
                "query": str,
                "property_id": str,
                "explanation": str,
            }
        """
        user_prompt = (
            f"User search query:\n{user_query}\n\n"
            f"Property details:\n{property_description}\n\n"
            "Explain why this property was recommended for the user's search."
        )

        response = self._llm.invoke(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ]
        )

        return {
            "query": user_query,
            "property_id": property_id,
            "explanation": response.content,
        }


# ---------------------------------------------------------------------------
# Quick test — run with: python explainability.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    TEST_QUERY = " "

    TEST_PROPERTY_ID = " "

    TEST_PROPERTY =""

    engine = ExplainabilityEngine()
    result = engine.explain(
        user_query=TEST_QUERY,
        property_id=TEST_PROPERTY_ID,
        property_description=TEST_PROPERTY,
    )

    print("Query      :", result["query"])
    print("Property ID:", result["property_id"])
    print("Explanation:\n", result["explanation"])