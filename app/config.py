import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from functools import lru_cache

load_dotenv()

class Settings(BaseSettings):
    keyspace: str = os.getenv("ASTRADB_KEYSPACE")
    client_id: str = os.getenv("ASTRADB_KEYSPACE")
    client_secret: str = os.getenv("ASTRADB_KEYSPACE")

    class Config:
        env_file = '.env'

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
