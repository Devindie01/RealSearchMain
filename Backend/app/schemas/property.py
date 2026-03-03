from pydantic import BaseModel, Field
from typing import Optional, List


class PropertyBase(BaseModel):
    title: str = Field(..., description="Title of the property listing")
    description: str = Field(..., description="Detailed description of the property")
    property_type: str = Field(
        ..., description="Type of the property (e.g., apartment, house)"
    )
    contract_type: str = Field(
        ..., description="Type of contract (e.g., for rent, for sale)"
    )
    price_lkr: float = Field(..., description="Price of the property in LKR")
    location: str = Field(..., description="Location of the property")
    bedrooms: Optional[int] = Field(None, description="Number of bedrooms")
    bathrooms: Optional[int] = Field(None, description="Number of bathrooms")
    land_size_sqm: Optional[float] = Field(
        None, description="Size of the land in square meters"
    )
    amenities: Optional[List[str]] = Field(
        None, description="List of amenities available with the property"
    )


class PropertyOwnerBase(BaseModel):
    owner_name: str = Field(..., description="Name of the property owner")
    owner_contact: str = Field(
        ..., description="Contact information of the property owner"
    )


class PropertyUpload(BaseModel):
    property: PropertyBase
    owner: PropertyOwnerBase


class PropertyCreate(PropertyUpload):
    """Schema for creating a property, inherits from Upload"""

    pass


class PropertyResponse(PropertyBase):
    """Schema for search results and data leaving the API"""

    id: Optional[str] = None
    created_by: Optional[str] = None
