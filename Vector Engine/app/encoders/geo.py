import numpy as np
from typing import Union, Tuple

class GeoEncoder:
    """
    Encodes latitude and longitude into a numeric vector.
    """
    def encode(self, geo: Union[Tuple[float, float], list, np.ndarray]) -> np.ndarray:
        """
        Accepts a tuple/list/array of (latitude, longitude) and returns a 2D vector.
        """
        if geo is None:
            return np.zeros(2, dtype=float)
        if isinstance(geo, (list, tuple, np.ndarray)) and len(geo) == 2:
            return np.array([float(geo[0]), float(geo[1])], dtype=float)
        raise ValueError("Geo must be a tuple/list/array of (latitude, longitude)")
