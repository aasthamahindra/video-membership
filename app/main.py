from fastapi import FastAPI
from cassandra.cqlengine.management import sync_table
from contextlib import asynccontextmanager
from .users.models import User
from . import db

DB_SESSION = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # triggers when FastAPI starts [@app.on_event deprecated]
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def homepage():
    return {"hello": "world"}
