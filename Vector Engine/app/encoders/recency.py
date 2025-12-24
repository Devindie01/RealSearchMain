from datetime import datetime, timedelta
import numpy as np

class RecencyEncoder:
    """
    Encodes a timestamp into a recency score between 0 and 1.
    """
    def __init__(self, period_days: int = 14, negative_filter: float = 0.0):
        self.period_days = period_days
        self.negative_filter = negative_filter

    def encode(self, timestamp: float) -> float:
        """
        Converts a Unix timestamp (seconds) into a recency score.
        Recent timestamps → 1.0
        Old timestamps → negative_filter
        """
        if timestamp is None:
            return self.negative_filter

        now = datetime.utcnow().timestamp()
        age_days = (now - timestamp) / 86400  # convert seconds to days
        if age_days >= self.period_days:
            return self.negative_filter
        # Linear decay: newer = 1, older = 0 (or negative_filter)
        return max(0.0, 1.0 - age_days / self.period_days)
