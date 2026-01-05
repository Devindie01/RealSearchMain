import numpy as np
from .base_space import Space
from app.encoders.numeric import NumericEncoder

class NumberSpace(Space):
    def __init__(self, fields: list, encoders: dict, weight: float = 1.0):
        super().__init__(fields, weight)
        self.encoders = encoders  # dict: field -> encoder

    def encode(self, obj):
        vectors = []
        for field in self.fields:
            value = getattr(obj, field, None)
            encoder = self.encoders[field]
            vectors.append(encoder.encode(value))
        combined = np.concatenate(vectors)
        return combined * self.weight
