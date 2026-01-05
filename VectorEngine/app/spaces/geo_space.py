import numpy as np
from typing import List
from app.encoders.geo import GeoEncoder


class GeoSpace:
    """
    Space for handling property geo coordinates.
    Encodes latitude and longitude using GeoEncoder.
    """

    def __init__(
        self, fields: List[str] = ["latitude", "longitude"], weight: float = 1.0
    ):
        self.fields = fields
        self.weight = weight
        self.encoder = GeoEncoder()

    def encode(self, property_obj) -> np.ndarray:
        """
        Encodes the property's latitude and longitude into a vector.
        Assumes property_obj has attributes 'latitude' and 'longitude'.
        """
        lat = getattr(property_obj, "latitude", 0.0)
        lon = getattr(property_obj, "longitude", 0.0)
        vec = self.encoder.encode((lat, lon))
        return vec * self.weight
