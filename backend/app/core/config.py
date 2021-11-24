from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    # App
    project_name: str = "Farmy"
    version: str = "1.0.0"
    api_prefix: str = "/api"
    secret_key: str = ""

    # DB
    DB_URL: str
    DB_NAME: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()