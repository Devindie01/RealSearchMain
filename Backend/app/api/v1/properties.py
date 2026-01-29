import json
import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
from app.schemas.property import PropertyCreate

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

DB_FILE = "temp_properties.json"


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


@router.post("/upload")
async def create_property(
    property_data: PropertyCreate,
    # current_user: str = Depends(get_current_user)
    current_user: str = "Guest",  # Temporary placeholder for testing purposes
):
    new_entry = property_data.dict()
    new_entry["created_by"] = current_user

    data = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    # 3. Append and Save
    data.append(new_entry)
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

    # This part only runs if the user is logged in!
    return {
        "message": f"Property '{property_data.property.title}' created by {current_user}",
        "data": property_data,
    }
