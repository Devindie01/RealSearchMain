import numpy as np

class WeightedSumAggregator:
    def aggregate(self, vectors, weights):
        combined = sum(v * w for v, w in zip(vectors, weights))
        return combined / np.linalg.norm(combined)
