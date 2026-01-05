import numpy as np
from .base_space import Space
from app.encoders.text import TextEncoder

class TextSpace(Space):
    def __init__(self, fields: list, weight: float = 1.0, model_name="all-MiniLM-L6-v2"):
        super().__init__(fields, weight)
        self.encoder = TextEncoder(model_name)

    def encode(self, obj):
        vectors = []
        for field in self.fields:
            value = getattr(obj, field, "")
            vectors.append(self.encoder.encode(value))
        combined = np.mean(vectors, axis=0)  # simple average
        return combined * self.weight
