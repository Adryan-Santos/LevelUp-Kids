from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Rotas da API
from app.api.v1.routes import parent, kid  # <- adicione kid aqui também se já tiver

app = FastAPI(title="LevelUp Kids")

# Caminho da pasta /static
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Servindo arquivos estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Incluindo rotas da API
app.include_router(parent.router)
app.include_router(kid.router)  # <- garante que a rota /v1/kid funcione

# ROTAS HTML
@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/login")
def login():
    return FileResponse(os.path.join(STATIC_DIR, "login.html"))

@app.get("/register")
def register():
    return FileResponse(os.path.join(STATIC_DIR, "register.html"))

@app.get("/about")
def about():
    return FileResponse(os.path.join(STATIC_DIR, "about.html"))

@app.get("/dashboard")
def dashboard():
    """Tela principal após login (seleção de heróis)"""
    return FileResponse(os.path.join(STATIC_DIR, "dashboard.html"))

@app.get("/ping")
def ping():
    return {"ok": True, "message": "LevelUp Kids API funcionando!"}
