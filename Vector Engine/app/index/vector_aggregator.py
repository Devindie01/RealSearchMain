import numpy as np

class VectorAggregator:
    def __init__(self, weights: dict = None):
        """
        weights: Optional dictionary specifying weights for each space.
                 e.g., {"text":1.0, "numeric":0.5, "geo":1.0, "recency":0.2, "image":1.5}
        """
        self.weights = weights or {}

    def aggregate(self, property_obj, spaces: dict) -> np.ndarray:
        """
        spaces: a dict of space_name -> vector/float output
        property_obj: your property dataclass (optional, if spaces need access)
        """
        vectors = []
        for name, vector in spaces.items():
            weight = self.weights.get(name, 1.0)
            vectors.append(np.array(vector) * weight)
        return np.concatenate(vectors)
