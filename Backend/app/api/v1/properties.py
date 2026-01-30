import json
import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
from app.models.property import Property, PropertyCreate
from app.models.user import User
from sqlmodel import Session, select
from app.db.session import get_session

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


DB_FILE = "temp_properties.json"


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            print("DEBUG: No 'sub' (email) found in token payload")
            raise credentials_exception
        return email
    except JWTError as e:
        # This will show the real reason (expired, invalid signature, etc.) in your console
        print(f"DEBUG: JWT Decode Error: {e}")
        raise credentials_exception


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def create_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_session),
    current_user_email: str = Depends(get_current_user),
):
    # 1. Verification: Get the actual User record from DB
    # (The dependency get_current_user already checked the JWT)
    user_statement = select(User).where(User.email == current_user_email)
    user = db.exec(user_statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User account not found in database",
        )

    # 2. Map the Frontend Data to the Database Model
    # We use data from property_data.property as per your nested schema
    new_property = Property(
        title=property_data.property.title,
        description=property_data.property.description,
        property_type=property_data.property.property_type,
        contract_type=property_data.property.contract_type,
        price_lkr=property_data.property.price_lkr,
        location=property_data.property.location,
        bedrooms=property_data.property.bedrooms,
        bathrooms=property_data.property.bathrooms,
        land_size_sqm=property_data.property.land_size_sqm,
        image_url=property_data.property.image_url,
        # LINKING: Assign the database User ID as the owner
        owner_id=user.id,
    )

    # 3. Save to Database
    try:
        db.add(new_property)
        db.commit()
        db.refresh(new_property)

        return {
            "message": f"Property '{new_property.title}' created successfully",
            "property_id": new_property.id,
            "owner": user.full_name,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save property to database",
        )
