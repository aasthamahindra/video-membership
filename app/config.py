import os
import pathlib
from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

BASE_DIR = pathlib.Path(__file__).resolve().parent
ENV_DIR = BASE_DIR / '.env'
load_dotenv(ENV_DIR) 

os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = "1"

class Settings(BaseSettings):
    keyspace: str = os.getenv('ASTRADB_KEYSPACE')

@lru_cache
def get_settings():
    return Settings()