from dataclasses import dataclass
from query.nlq.query_intent import QueryIntent

@dataclass
class Query:
    raw_query: str
    intent: QueryIntent
