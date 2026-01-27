from typing import Any
from fastapi import APIRouter, Depends
from app import schemas, models
from app.api.v1 import deps

router = APIRouter()

@router.get("/me", response_model=schemas.user.User)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user