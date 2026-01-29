from typing import Optional, List, TYPE_CHECKING
from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel, Field, Relationship

# Only import Property for type hinting to avoid circular imports
if TYPE_CHECKING:
    from .property import Property

# 1. SHARED FIELDS (The "Base")
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, nullable=False)
    full_name: Optional[str] = None
    is_active: bool = Field(default=True)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return v.lower().strip()

# 2. FOR SIGNUP (Input)
class UserCreate(UserBase):
    password: str  # Plain text from the user

# 3. FOR RESPONSES (Output)
class UserPublic(UserBase):
    id: int

# 4. THE DATABASE TABLE (The "Model")
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    
    # Relationship to the Property model (One-to-Many)
    properties: List["Property"] = Relationship(back_populates="owner")

# 5. TOKEN SCHEMA
class Token(SQLModel):
    access_token: str
    token_type: str