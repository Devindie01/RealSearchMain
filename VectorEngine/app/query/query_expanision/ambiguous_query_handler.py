import os
import pandas as pd
import numpy as np
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from dotenv import load_dotenv

load_dotenv()
from sentence_transformers import SentenceTransformer
import faiss

# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME1 = "arcee-ai/trinity-large-preview:free"

llm = ChatOpenAI(
    model=MODEL_NAME1,
    temperature=0.2,
    base_url=BASE_URL,
    api_key="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",
)
SYSTEM_PROMPT_QNA = """
You are a domain-constrained real estate reasoning agent for Sri Lanka.

PRIMARY GOAL:
Reduce ambiguity in an ambiguous real estate query by generating multiple plausible, concrete interpretations that reflect different reasonable user intents.

IMPORTANT:
Your goal is NOT to find the single best interpretation.
Your goal is to surface DIFFERENT valid interpretations that could realistically match the same ambiguous query.
INTERNAL REASONING (do this silently):
1. Identify multiple plausible user intents (not just one).
2. For each intent, infer:
   - Property usage (living, renting, investing, hospitality).
   - Location context (urban, suburban, beach, hill country).
   - Property type (apartment, house, land, hotel).
3. Map each intent to dataset-realistic real estate attributes.
4. Ensure all features exist in real Sri Lankan listings.

DIVERSITY RULE (VERY IMPORTANT):
Each candidate query MUST differ meaningfully in at least ONE of:
- Location type (e.g., urban vs beach vs hill country)
- Property type (apartment vs house vs land vs hotel)
- Use case (residential living vs investment vs hospitality)
- Scale (compact apartment vs large land vs multi-bedroom property)
LOCATION VARIATION (use different regions where plausible):
- Beach towns: Mirissa, Bentota, Unawatuna, Hikkaduwa, Negombo
- Hill country: Kandy, Nuwara Eliya, Ella, Hatton
- Urban centers: Colombo, Galle, Jaffna
- Suburban areas: Battaramulla, Rajagiriya, Maharagama

RULES:
- Stay strictly within real estate domain.
- Use only dataset-realistic attributes (bedrooms, bathrooms, land size, amenities, views, parking, floor).
- Avoid emotional, lifestyle, or abstract language.
- Do NOT invent features or infrastructure not found in listings.
- Do NOT collapse candidates into minor variations.

OUTPUT FORMAT (STRICT JSON):
{
  "reasoning_summary": "<brief factual summary of the ambiguous intent space>",
  "candidate_queries": [
    "<expanded query representing interpretation A>",
    "<expanded query representing interpretation B>",
    "<expanded query representing interpretation C>"
  ]
}

Each candidate query must be:
- Concrete
- Dataset-realistic
- Clearly different in intent or context from the others
"""

USER_PROMPT_QNA = """
Ambiguous query:
"{query}"
"""

SYSTEM_PROMPT_REFLECTION = """
You are a real estate query reflection and validation agent for Sri Lanka.

TASK:
Evaluate whether the proposed expanded queries successfully reduce ambiguity.

VALIDATION CRITERIA:
- Each query must be concrete and specific.
- Must use real-estate features found in listings.
- Must clearly resolve location, property type, and key attributes.
- Must NOT contain abstract, lifestyle, or vague wording.
- Must be suitable for direct dataset filtering.

OUTPUT FORMAT (STRICT JSON):
{
  "approved": true | false,
  "issues": ["issue1", "issue2"],
  "suggestion": "<how to improve if not approved>"
}

If ANY query is ambiguous → approved = false.
"""

USER_PROMPT_REFLECTION = """
Original ambiguous query:
"{original_query}"

Candidate expanded queries:
{candidate_queries}
"""


def run_qna_agent(query: str) -> dict:
    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT_QNA),
            HumanMessage(content=USER_PROMPT_QNA.format(query=query)),
        ]
    )
    return json.loads(response.content)


def run_reflection_agent(original_query: str, candidate_queries: list) -> dict:
    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT_REFLECTION),
            HumanMessage(
                content=USER_PROMPT_REFLECTION.format(
                    original_query=original_query,
                    candidate_queries="\n".join(candidate_queries),
                )
            ),
        ]
    )
    return json.loads(response.content)


def expand_and_bound_ambiguous_query(query: str, max_iterations: int = 3):
    iteration = 0
    last_result = None

    while iteration < max_iterations:
        print(f"\n🔁 Iteration {iteration + 1}")
        print("Ambiguous Query:", query)

        qna_result = run_qna_agent(query)
        reasoning = qna_result["reasoning_summary"]
        candidate_queries = qna_result["candidate_queries"]

        print("\nCandidate Queries:")
        for q in candidate_queries:
            print("-", q)

        reflection = run_reflection_agent(query, candidate_queries)

        if reflection["approved"]:
            print("\n✅ Reflection Approved")
            return candidate_queries

        # Feed reflection feedback back into query
        query = f"{query}. Clarification: {reflection['suggestion']}"
        last_result = candidate_queries
        iteration += 1

    return last_result
