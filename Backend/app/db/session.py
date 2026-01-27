from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 1. Create the Database Engine
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

# 2. Create the SessionLocal class (Interface to talk to DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. The Dependency function used in your API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()