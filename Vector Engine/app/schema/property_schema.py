from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Property:
    """
    Canonical Property schema.
    This schema is encoder-aware but encoder-agnostic.
    """

    # IDENTIFIERS (NOT ENCODED)
    id: str
    url: str

    # TEXT FIELDS → TextEncoder (Semantic Embeddings)
    title: str
    location: str
    description: str
    full_description: str

    # NUMERIC FIELDS → NumericEncoder (Scaled / Bucketed)
    price_lkr: float
    size_perches: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None

    # GEO FIELDS → Geo Metadata / Geo Index (NOT Text/Numeric)
    latitude: float = 0.0
    longitude: float = 0.0

    # CATEGORICAL FIELDS → CategoricalTextEncoder
    # (Encoded as TEXT, not one-hot)
    property_type: str = ""  # House / Apartment / Land
    land_type: Optional[str] = None  # Residential / Agricultural
    contract_type: str = ""  # Sale / Rent

    # METADATA FIELDS (STORED, NOT ENCODED)
    amenities: List[str] = field(default_factory=list)
    images: List[str] = field(default_factory=list)
