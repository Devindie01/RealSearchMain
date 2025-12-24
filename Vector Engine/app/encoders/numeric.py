import numpy as np
from .base import Encoder

class NumericEncoder(Encoder):
    def __init__(self, min_val: float, max_val: float):
        self.min = min_val
        self.max = max_val

    def encode(self, value: float) -> np.ndarray:
        if value is None:
            return np.zeros(1)
        normalized = (value - self.min) / (self.max - self.min)
        return np.array([normalized])
