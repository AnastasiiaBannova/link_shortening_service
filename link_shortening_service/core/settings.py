import os
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    # Common
    MICROSERVICE_NAME: str
    DEBUG: bool

    # Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: Optional[str]
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    BASE_URL: str

    class Config:
        env_file = os.getenv('ENV', '.env')


settings = Settings()
