from sqlmodel import SQLModel, Session, create_engine
from typing import Generator
from app.core.config import settings # Assuming Settings is moved to config.py

# Use the URL from your settings
database_url = settings.DATABASE_URL

connect_args = {}

if database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(database_url, connect_args=connect_args)

def init_db():
    # Importing here prevents circular imports and registers models
    from app.models.user import User
    from app.models.property import Property

    # Create tables in the Docker Postgres instance
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session