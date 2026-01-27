import os
from datetime import timedelta

class Settings:
    SECRET_KEY: str = "SUPER_SECRET_CHEF_KEY_123" # In production, use an environment variable
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()