from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import kid_mission as kid_mission_repo
from app.repositories import mission as mission_repo
from app.services.kid import add_experience
from app.schemas.kid_mission import KidMissionCreate

# Completar missão
def complete_mission(db: Session, data: KidMissionCreate):
    mission = mission_repo.get_mission_by_id(db, data.mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Missão não encontrada.")

    # Registra missão concluída e adiciona XP/gold
    kid_mission = kid_mission_repo.create_kid_mission(db, data)
    add_experience(db, data.kid_id, mission.xp, 10)  # gold fixo opcional
    return kid_mission

# Listar missões concluídas por Kid
def list_completed_missions(db: Session, kid_id: int):
    return kid_mission_repo.get_kid_missions_by_kid(db, kid_id)
