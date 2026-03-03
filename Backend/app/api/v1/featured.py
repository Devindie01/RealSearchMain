from fastapi import APIRouter
# from app.services.search_service import SearchService
from app.models.search import SearchRequest
from typing import Dict, Any
import uuid

router = APIRouter()

@router.get("/featured", response_model=Dict[str, Any])
async def get_featured_properties():
    # Use a fixed query to get "featured" items via vector search
    # We use a random UUID for the request ID as it's an internal call
    # request_id = str(uuid.uuid4())
    
    # # "Best Properties" or "Luxury" or "Featured" - choice of query
    # search_query = SearchRequest(query="Apartments in Colombo")
    
    # search_service = SearchService()
    
    # properties, count = await search_service.search(
    #     request=search_query,
    #     request_id=request_id
    # )
    # print(f"Featured properties retrieved: {properties}")
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
