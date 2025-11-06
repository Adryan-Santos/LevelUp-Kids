import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.routes import parent, kid, mission, reward, kid_mission, kid_reward

app = FastAPI(title="LevelUp Kids")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Rotas da API
app.include_router(parent.router)
app.include_router(kid.router)
app.include_router(mission.router)
app.include_router(reward.router)
app.include_router(kid_mission.router)
app.include_router(kid_reward.router)

# Páginas do front-end
def serve_page(filename: str):
    path = os.path.join(STATIC_DIR, filename)
    if os.path.exists(path):
        return FileResponse(path)
    return {"error": "Página não encontrada."}

@app.get("/")
def index():
    return serve_page("index.html")

@app.get("/login")
def login():
    return serve_page("login.html")

@app.get("/register")
def register():
    return serve_page("register.html")

@app.get("/dashboard")
def dashboard():
    return serve_page("dashboard.html")

@app.get("/manage")
def manage():
    return serve_page("manage.html")

@app.get("/hero")
def hero():
    return serve_page("hero.html")

@app.get("/about")
def about():
    return serve_page("about.html")

@app.get("/ping")
def ping():
    return {"ok": True, "message": "LevelUp Kids API funcionando!"}
