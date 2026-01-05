from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.query.query_object import QuerySegment
from sentence_transformers import SentenceTransformer

from dotenv import load_dotenv
import os

load_dotenv()


class QueryEmbedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def get_vector(self, text: str):
        return self.model.encode(text).tolist()


def get_chain():
    llm = ChatOpenAI(
        model="mistralai/devstral-2512:free",
        temperature=0,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
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
