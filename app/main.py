import dotenv

# Load .env variables into environment before any LangChain imports
dotenv.load_dotenv()
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers.product_router import (
    router as product_router,
)
from app.routers.recommendation_router import (
    router as recommendation_router,
)
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from app.routers.auth_router import router as auth_router
from app.routers.admin_router import router as admin_router
from app.routers.event_router import router as event_router

app = FastAPI(title="SmartReco")


templates = Jinja2Templates(directory="app/templates")

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)
@app.get("/", response_class=HTMLResponse)
def root_home_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={"request": request}
    )

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(admin_router)
app.include_router(event_router)
app.include_router(
    recommendation_router
)

@app.get("/")
def home():
    return {"message": "SmartReco API Running"}