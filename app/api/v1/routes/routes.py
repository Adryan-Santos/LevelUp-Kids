from fastapi import APIRouter
from app.api.v1.routes import parent, kid, mission, reward, kid_mission, kid_reward

api_router = APIRouter()

# Inclui todas as rotas da API
api_router.include_router(parent.router, prefix="/parents", tags=["Parents"])
api_router.include_router(kid.router, prefix="/kids", tags=["Kids"])
api_router.include_router(mission.router, prefix="/missions", tags=["Missions"])
api_router.include_router(reward.router, prefix="/rewards", tags=["Rewards"])
api_router.include_router(kid_mission.router, prefix="/kid_missions", tags=["Kid Missions"])
api_router.include_router(kid_reward.router, prefix="/kid_rewards", tags=["Kid Rewards"])
