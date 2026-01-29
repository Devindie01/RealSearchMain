from fastapi import APIRouter, Header, Query
from app.schemas.property import PropertyResponse 
from app.services.search_service import SearchService
from typing import List, Optional
import uuid

router = APIRouter()

@router.get("/search", response_model=List[PropertyResponse])
async def nlp_search(
    query: str, 
    x_session_id: Optional[str] = Header(None)
):
    # If no session ID exists, we create a temporary one to track behavior
    session_id = x_session_id or str(uuid.uuid4())
    
    results = await SearchService.search_nlp(query, session_id)
    return results