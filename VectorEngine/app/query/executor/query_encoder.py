from langchain_openai import OpenAIEmbeddings
import os

class QueryEmbedder:
    def __init__(self, model: str = "text-embedding-3-small"):
        # You can also specify 'dimensions' here if your Weaviate 
        # collection expects a specific size (e.g., 512, 1024)
        self.embeddings = OpenAIEmbeddings(model=model)

    def get_vector(self, text: str) -> list[float]:
        """Converts a string into a vector embedding."""
        if not text.strip():
            # If the description is empty, return a zero-vector 
            # or handle it based on your search logic
            return []
            
        # .embed_query is optimized for single search strings
        return self.embeddings.embed_query(text)