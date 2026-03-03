from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from sqlmodel import SQLModel
from app.db.base_class import Base

from typing import Optional, List, TYPE_CHECKING
from pydantic import Field as PydanticField
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User

# SHARED FIELDS (The "Base")
class PropertyBase(SQLModel):
    title: str = Field(index=True)
    description: str
    property_type: str  # e.g., House, Apartment
    contract_type: str  # e.g., For Sale, For Rent
    price_lkr: float = Field(index=True)
    location: str
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    land_size_sqm: Optional[float] = None
    image_url: Optional[str] = None

#FOR UPLOAD (Input from Frontend)
class PropertyOwnerBase(SQLModel):
    owner_name: str
    owner_contact: str

class PropertyCreate(SQLModel):
    property: PropertyBase
    owner: PropertyOwnerBase

# For response
class PropertyPublic(PropertyBase):
    id: int
    owner_id: int

# The actual database model
class Property(PropertyBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Link to the User who created it
    owner_id: int = Field(foreign_key="user.id", nullable=False)
    
    # Relationship back to User model
    owner: Optional["User"] = Relationship(back_populates="properties")