from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers.product_router import (
    router as product_router,
)
from app.routers.auth_router import router as auth_router

app = FastAPI(title="SmartReco")


templates = Jinja2Templates(directory="app/templates")

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

app.include_router(auth_router)
app.include_router(product_router)

@app.get("/")
def home():
    return {"message": "SmartReco API Running"}