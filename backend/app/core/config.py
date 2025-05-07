# Reference: https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/core/config.py

import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    SECRET_KEY: str = secrets.token_urlsafe(32)

    PROJECT_NAME: str = "tokenblood"

    SQLITE_LOCATION: str = "../db.sqlite"
    SQLALCHEMY_DATABASE_URL: str = f"sqlite:///{SQLITE_LOCATION}"

    OPENAI_MODEL_NAME: str
    OPENAI_API_KEY: str


settings = Settings()  # type: ignore


# required for ai/ package
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
os.environ["OPENAI_MODEL_NAME"] = settings.OPENAI_MODEL_NAME
