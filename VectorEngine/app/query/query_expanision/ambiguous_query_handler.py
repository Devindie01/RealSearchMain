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

BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME1 = "google/gemini-2.5-flash-lite-preview-09-2025"

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
- Scale (compact vs spacious vs large-scale property)



RULES:
- Stay strictly within real estate domain.
- Use descriptive, relative terms for scale (e.g., compact, spacious, large) — do NOT specify exact bedroom or bathroom counts.
- Use only dataset-realistic attributes (land size, amenities, views, parking, floor, layout type).
- If ambigous query a;ready has ant of property_type, price, location, contract_type,land_size, no_of_bedrooms,no_of_bathrooms entities, make sure to preserve them in all candidate queries.
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
- Concrete and dataset-realistic
- Focused on property type, location, usage, and key amenities
- Free of exact numeric constraints on bedrooms or bathrooms
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
    print(f"    🤖 QnA agent — sending query to LLM...")
    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT_QNA),
            HumanMessage(content=USER_PROMPT_QNA.format(query=query)),
        ]
    )
    print(f"    ✅ QnA agent — response received ({len(response.content)} chars)")

    # Strip markdown code fences if present
    content = response.content.strip()
    content = content.replace("```json", "").replace("```", "").strip()

    if not content:
        raise ValueError(
            "LLM returned empty response — query may be invalid or too vague"
        )

    result = json.loads(content)
    print(f"    📋 Reasoning: {result.get('reasoning_summary', '')[:120]}...")
    return result


def run_reflection_agent(original_query: str, candidate_queries: list) -> dict:
    print(
        f"    🔍 Reflection agent — validating {len(candidate_queries)} candidates..."
    )
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
    print(
        f"    ✅ Reflection agent — response received ({len(response.content)} chars)"
    )

    # Strip markdown code fences if present
    content = response.content.strip()
    content = content.replace("```json", "").replace("```", "").strip()

    if not content:
        raise ValueError("Reflection agent returned empty response")

    result = json.loads(content)
    approved = result.get("approved", False)
    issues = result.get("issues", [])
    suggestion = result.get("suggestion", "")

    print(f"    {'✅ Approved' if approved else '❌ Not approved'}")
    if not approved:
        print(f"    ⚠️  Issues: {issues}")
        print(f"    💡 Suggestion: {suggestion[:120]}...")
    return result


def expand_and_bound_ambiguous_query(query: str, max_iterations: int = 3):
    print(f"\n  🔀 Expanding ambiguous query (max {max_iterations} iterations)...")
    print(f"  Original: {query[:120]}...")

    iteration = 0
    last_result = None

    while iteration < max_iterations:
        print(f"\n  🔁 Iteration {iteration + 1}/{max_iterations}")

        qna_result = run_qna_agent(query)
        candidate_queries = qna_result["candidate_queries"]

        print(f"\n  📝 Candidate queries ({len(candidate_queries)}):")
        for i, q in enumerate(candidate_queries, 1):
            print(f"    [{i}] {q[:120]}...")

        reflection = run_reflection_agent(query, candidate_queries)

        if reflection["approved"]:
            print(f"\n  ✅ Expansion approved on iteration {iteration + 1}")
            return candidate_queries

        query = f"{query}. Clarification: {reflection['suggestion']}"
        print(f"\n  🔄 Retrying with clarified query: {query[:120]}...")
        last_result = candidate_queries
        iteration += 1

    print(f"\n  ⚠️  Max iterations reached — returning last result")
    return last_result