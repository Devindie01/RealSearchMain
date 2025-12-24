import numpy as np
from typing import List, Optional
from app.encoders.recency import RecencyEncoder

class RecencySpace:
    """
    Space for handling property recency.
    Combines multiple timestamps of a property into a single score.
    """
    def __init__(
        self,
        period_days: int = 14,
        negative_filter: float = 0.0,
        weight: float = 1.0,
        aggregation_mode: str = "average",  # "average", "min", "max"
    ):
        self.encoder = RecencyEncoder(period_days, negative_filter)
        self.weight = weight
        self.aggregation_mode = aggregation_mode

    def encode(self, property_obj) -> float:
        """
        Encodes all timestamps of a property and returns a combined recency score.
        property_obj must have attribute 'timestamp_list' as list of Unix timestamps (seconds).
        """
        timestamps: List[Optional[float]] = getattr(property_obj, "timestamp_list", [])
        if not timestamps:
            return 0.0 * self.weight

        scores = [self.encoder.encode(ts) for ts in timestamps]

        if self.aggregation_mode == "min":
            combined = min(scores)
        elif self.aggregation_mode == "max":
            combined = max(scores)
        else:  # default average
            combined = sum(scores) / len(scores)

        return combined * self.weight
