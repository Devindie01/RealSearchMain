from fastapi import APIRouter

from app.api.v1 import auth, users, properties, search

api_router = APIRouter()

# 1. User Authentication (Login/Register)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# 2. User Profile (Get Current User)
api_router.include_router(users.router, prefix="/users", tags=["users"])

# 3. Properties (The main inventory: Load, Add, Details)
api_router.include_router(properties.router, prefix="/properties", tags=["properties"])

# 4. Search (Basic & Semantic)
api_router.include_router(search.router, prefix="/search", tags=["search"])