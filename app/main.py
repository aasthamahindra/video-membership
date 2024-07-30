import pathlib
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from cassandra.cqlengine.management import sync_table
from contextlib import asynccontextmanager
from .users.models import User
from . import db
from fastapi.templating import Jinja2Templates

BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"

DB_SESSION = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # triggers when FastAPI starts [@app.on_event deprecated]
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)
    yield

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

# In general, FastAPI gives JSON responses [REST API],
# but to render HTML response we use 'response_class' as HTMLResponse
@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    context = {
        "request": request,
        "user": "Aastha"
    }
    return templates.TemplateResponse("home.html", context=context)

@app.get("/users")
def users_list_view():
    query = User.objects.all().limit(10)
    return list(query)

@app.post("/create-user")
def create_user(email: str, password: str):
    query = User.create_user(email, password)
    return query
