import os
from typing import List

from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    APP_NAME: str = "Mental Health Chatbot"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret-change-me")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ALGORITHM: str = "HS256"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"]
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./backend.db")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
