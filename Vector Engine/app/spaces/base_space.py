from abc import ABC, abstractmethod
import numpy as np

class Space(ABC):
    def __init__(self, fields: list, weight: float = 1.0):
        self.fields = fields
        self.weight = weight

    @abstractmethod
    def encode(self, obj) -> np.ndarray:
        """Take a property object and return a vector"""
        pass
