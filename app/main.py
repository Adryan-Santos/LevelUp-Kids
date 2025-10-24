from fastapi import FastAPI
from app.api.v1.routes.parent import router as parent_router
from app.api.v1.routes.kid import router as kid_router
from app.api.v1.routes.mission import router as mission_router
from app.api.v1.routes.reward import router as reward_router

app = FastAPI(title="LevelUp Kids API")

# Rotas
app.include_router(parent_router)
app.include_router(kid_router)
app.include_router(mission_router)
app.include_router(reward_router)

@app.get("/")
def root():
    return {"ok": True, "message": "LevelUp Kids API!"}
