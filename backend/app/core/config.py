# Reference: https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/core/config.py

import secrets

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    SECRET_KEY: str = secrets.token_urlsafe(32)

    PROJECT_NAME: str = "tokenblood"
    SQLITE_LOCATION: str = "../db.sqlite"
    OPENAI_MODEL_NAME: str
    OPENAI_API_KEY: str


settings = Settings()  # type: ignore

assert load_dotenv(verbose=True)  # required for ai/ package
