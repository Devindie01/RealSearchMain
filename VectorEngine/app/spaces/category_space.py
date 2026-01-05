from typing import List, Optional
import numpy as np
from app.encoders.categorical import CategoricalTextEncoder

class CategorySpace:
    """
    Space for multiple categorical fields (property_type, land_type, contract_type).
    Encodes categories using CategoricalTextEncoder and combines vectors.
    """
    def __init__(
        self,
        fields: List[str],
        categories: Optional[List[str]] = None,
        weight: float = 1.0,
        model_name: str = "all-MiniLM-L6-v2",
        uncategorized_as_category: bool = True,
    ):
        self.fields = fields
        self.weight = weight
        self.encoder = CategoricalTextEncoder(model_name)
        self.categories = categories or []
        self.uncategorized_as_category = uncategorized_as_category

    def encode(self, obj) -> np.ndarray:
        vectors = []
        for field in self.fields:
            value = getattr(obj, field, "")
            # Handle unknown categories
            if value not in self.categories and self.uncategorized_as_category:
                value = "other"
            vectors.append(self.encoder.encode(str(value)))
        combined = np.mean(vectors, axis=0)  # average across fields
        return combined * self.weight
