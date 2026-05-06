from pydantic import BaseModel, Field
from typing import Optional


class QuerySegment(BaseModel):
    # description: str = Field(
    #     description="All subjective or textual features not covered by other fields (e.g., 'modern interior', 'quiet neighborhood', 'near a park')."
    # )
    property_type: Optional[list[str]] = Field(
        description="e.g., 'apartment', 'house', 'land', 'commercial','villa','hotel', etc."
    )
    contract_type: Optional[str] = Field(description="e.g., 'for rent', 'for sale'")
    price_min: Optional[float] = Field(description="The minimum price mentioned.")
    price_max: Optional[float] = Field(description="The maximum price mentioned.")
    price_unit: Optional[str] = Field(description="Currency unit for the price, e.g., 'LKR', 'USD'.") #check the currency type and filter
    price_period: Optional[str] = Field(description="If the price is for rent/lease, the period it applies to, e.g., 'per month', 'per year'.")
    location: Optional[list[str]]= Field(description="City, neighborhood, or specific area.")
    no_of_bedrooms: Optional[int] = Field(description="Number of bedrooms.")
    no_of_bathrooms: Optional[int] = Field(description="Number of bathrooms.")
    land_size: Optional[float] = Field(description="Size of the land or property area.")

    #per perch kind of values handle