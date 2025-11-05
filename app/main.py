from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.api.v1.routes import parent, kid
from app.api.v1.routes import mission as mission_routes
from app.api.v1.routes import reward as reward_routes

app = FastAPI(title="LevelUp Kids")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# APIs
app.include_router(parent.router)
app.include_router(kid.router)
app.include_router(mission_routes.router)
app.include_router(reward_routes.router)

# Páginas
@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/login")
def login():
    return FileResponse(os.path.join(STATIC_DIR, "login.html"))

@app.get("/register")
def register():
    return FileResponse(os.path.join(STATIC_DIR, "register.html"))

@app.get("/dashboard")
def dashboard():
    return FileResponse(os.path.join(STATIC_DIR, "dashboard.html"))

@app.get("/manage")
def manage():
    return FileResponse(os.path.join(STATIC_DIR, "manage.html"))

@app.get("/hero")
def hero():
    return FileResponse(os.path.join(STATIC_DIR, "hero.html"))

@app.get("/about")
def about():
    return FileResponse(os.path.join(STATIC_DIR, "about.html"))

@app.get("/ping")
def ping():
    return {"ok": True, "message": "LevelUp Kids API funcionando!"}
