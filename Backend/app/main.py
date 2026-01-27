# app/main.py (updated)
from fastapi import FastAPI
from app.api import search, auth, properties

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(search.router, prefix="/api/v1", tags=["Search"])
app.include_router(properties.router, prefix="/api/v1", tags=["Properties"])