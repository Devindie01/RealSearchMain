from pydantic import BaseModel, Field
from typing import Optional

class QuerySegment(BaseModel):
    description: str = Field(description="All subjective or textual features not covered by other fields (e.g., 'modern interior', 'quiet neighborhood', 'near a park').")
    property_type: Optional[str] = Field(description="e.g., 'apartment', 'house', 'land', 'commercial','villa','hotel', etc.")
    contract_type: Optional[str] = Field(description="e.g., 'for rent', 'for sale'")
    price: Optional[float] = Field(description="The maximum budget or price mentioned.")
    location: Optional[str] = Field(description="City, neighborhood, or specific area.")
    no_of_bedrooms: Optional[int] = Field(description="Number of bedrooms.")
    no_of_bathrooms: Optional[int] = Field(description="Number of bathrooms.")
    land_size: Optional[float] = Field(description="Size of the land or property area.")
