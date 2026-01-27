from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class SearchQuery(BaseModel):
    description: str = Field(..., example="Luxury villa with a pool in Los Angeles")
    
    property_type: Optional[str] = Field(None, example="e.g., 'apartment', 'house', 'land', 'commercial','villa','hotel', etc.")
    contract_type: Optional[str] = Field(None, example="e.g., 'for rent', 'for sale'")
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    location: Optional[str] = Field(None, example="San Francisco, CA")
    no_bedrooms: Optional[int] = None
    no_bathrooms: Optional[int] = None
    land_size: Optional[float] = None

