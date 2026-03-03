from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1 import featured
from app.db.session import init_db
from app.api.v1 import auth
from app.api.v1 import search, auth, properties
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Authentication API"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000","http://localhost:3001"], # Add both common local addresses
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(search.router, prefix="/api/v1", tags=["Search"])
app.include_router(properties.router, prefix="/api/v1", tags=["Properties"])
app.include_router(featured.router, prefix="/api/v1", tags=["Featured"])
