from abc import ABC, abstractmethod
import numpy as np

class Encoder(ABC):
    @abstractmethod
    def encode(self, value) -> np.ndarray:
        """Convert a value to a vector representation"""
        pass
