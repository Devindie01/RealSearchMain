from sentence_transformers import SentenceTransformer
from .base import Encoder
import numpy as np

class TextEncoder(Encoder):
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, text: str) -> np.ndarray:
        if not text:
            text = ""
        return np.array(self.model.encode(text))
