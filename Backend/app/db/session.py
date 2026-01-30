from sqlmodel import SQLModel, Session, create_engine
from typing import Generator
from app.core.config import settings

# 1. Use the URL from your .env/settings
sqlite_url = settings.SQLALCHEMY_DATABASE_URL

# 2. Only use check_same_thread for SQLite
connect_args = {}
if sqlite_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, connect_args=connect_args)


def init_db():
    # 3. CRITICAL: Import your models here.
    # This "registers" the tables with SQLModel.metadata
    from app.models.user import User
    from app.models.property import Property

    # from app.models.property import Property

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
