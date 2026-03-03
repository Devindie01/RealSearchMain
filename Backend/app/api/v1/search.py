from fastapi import APIRouter, Header, Body
from app.models.search import SearchRequest
from app.models.property import PropertyPublic
# from app.services.search_service import SearchService
from typing import List, Optional, Dict, Any
import uuid

router = APIRouter()

# Using Dict for now if PropertyResponse/PropertyPublic structure is strict or mismatching dummy data
# But plan says PropertyResponse. Let's try to match PropertyPublic or return dict.
# For now, returning Dict is safer given the dummy data structure in service.
@router.post("/search", response_model=Dict[str, Any])
async def search_properties(
    request: SearchRequest,
    x_request_id: Optional[str] = Header(None),
):
    # Generate a unique request ID if not provided
    # if not x_request_id:
    #     x_request_id = str(uuid.uuid4())
    
    # search_service = SearchService()
    # properties, count = await search_service.search(
    #     request=request,
    #     request_id=x_request_id
    # )

    properties = [
    {
      "id": 1,
      "title": "Modern Downtown Loft",
      "location": "Colombo 03, Sri Lanka",
      "price": 45000000,
      "bedrooms": 2,
      "bathrooms": 2,
      "sqft": 1200,
      "image": "/modern-loft-interior.jpg",
      "type": "Apartment",
      "lat": 6.9271,
      "lng": 79.8612,
      "insight": "Prime business district location with high rental yields"
    },
    {
      "id": 2,
      "title": "Luxury Waterfront Condo",
      "location": "Mount Lavinia, Sri Lanka",
      "price": 52000000,
      "bedrooms": 2,
      "bathrooms": 2,
      "sqft": 1200,
      "image": "/modern-loft-interior.jpg",
      "type": "Apartment",
      "lat": 6.9271,
      "lng": 79.8612,
      "insight": "Prime business district location with high rental yields"
    }
    ]
    # print (properties)
    count = len(properties)
    return {"results": properties, "totalCount": count}
