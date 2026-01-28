from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import init_db
from app.api.v1 import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Authentication API"}
