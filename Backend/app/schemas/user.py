from pydantic import BaseModel, EmailStr
from typing import Optional

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to return to client (NEVER return the password)
class UserPublic(UserBase):
    id: int
    
    class Config:
        from_attributes = True

# Schema for the Login Token
class Token(BaseModel):
    access_token: str
    token_type: str
