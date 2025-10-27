from fastapi import FastAPI
from app.api.v1.routes.parent import router as parent_router

app = FastAPI(title="LevelUp Kids")

# Rotas
app.include_router(parent_router)

@app.get("/")
def root():
    return {"ok": True, "message": "LevelUp Kids API!"}
