import dspy
from pydantic import BaseModel, Field
from typing import Optional

class QueryIntent(BaseModel):
    search_text: str = Field(description="Main semantic search term")
    recency_weight: float = Field(description="Freshness importance (0 to 1)")
    category_filter: Optional[str] = None


class NLQToIntent(dspy.Signature):
    raw_query = dspy.InputField()
    intent = dspy.OutputField(desc="Structured QueryIntent")


lm = dspy.OpenAI(model="gpt-4")
dspy.settings.configure(lm=lm)


def extract_intent(nlq: str) -> QueryIntent:
    predictor = dspy.TypedPredictor(NLQToIntent)
    result = predictor(raw_query=nlq)
    return result.intent
