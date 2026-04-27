from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.query.query_object import QuerySegment
from sentence_transformers import SentenceTransformer

from dotenv import load_dotenv
import os

load_dotenv()


class QueryEmbedder:
    def __init__(self, model_name="Snowflake/snowflake-arctic-embed-l-v2.0"):
        self.model = SentenceTransformer(model_name)

    def get_vector(self, text: str):
        return self.model.encode(text).tolist()


def get_chain():
    llm = ChatOpenAI(
        model="google/gemini-2.0-flash-lite-001",
        temperature=0,
        openai_api_key="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",
        openai_api_base="https://openrouter.ai/api/v1",
    )

    # 2. Structured output
    structured_llm = llm.with_structured_output(QuerySegment)

    # 3. Prompt
    prompt = ChatPromptTemplate.from_template(
        "Extract all relevant property search parameters from the following user query: {input}"
    )

    # 4. Chain
    chain = prompt | structured_llm
    return chain


# Global chain - initialize only when needed
chain = get_chain()


def initialize_chain():
    global chain
    if chain is None:
        chain = get_chain()
    return chain