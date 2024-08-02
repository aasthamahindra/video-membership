import pathlib
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from cassandra.cqlengine.management import sync_table
from contextlib import asynccontextmanager

from .users.models import User
from .users.schemas import UserSignUpSchema
from . import db


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

@app.get("/sign-in", response_class=HTMLResponse)
def login_get_view(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("auth/signin.html", context=context)

@app.post("/sign-in", response_class=HTMLResponse)
def login_post_view(request: Request, email: str=Form(...), password: str=Form(...)):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("auth/signin.html", context=context)

@app.get("/sign-up", response_class=HTMLResponse)
def signup_get_view(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("auth/signup.html", context=context)

@app.post("/sign-up", response_class=HTMLResponse)
def signup_post_view(request: Request, username: str=Form(...), email: str=Form(...), password: str=Form(...), password_confirm: str=Form(...)):
    cleaned_data = UserSignUpSchema(username=username, email=email, password=password, password_confirm=password_confirm)
    print(cleaned_data.model_dump())
    context = {
        "request": request,
    }
    return templates.TemplateResponse("auth/signup.html", context=context)

@app.get("/users")
def users_list_view():
    query = User.objects.all().limit(10)
    return list(query)

@app.post("/create-user")
def create_user(email: str, password: str):
    query = User.create_user(email, password)
    return query
