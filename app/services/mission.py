from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import mission as mission_repo
from app.repositories import kid_mission as kid_mission_repo

#Criar missão (somente Parent)
def create_mission(db: Session, data):
    return mission_repo.create_mission(db, data)

#Editar missão (somente Parent)
def update_mission(db: Session, mission_id: int, updated_data: dict, parent_id: int):
    mission = mission_repo.get_mission_by_id(db, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Missão não encontrada.")
    if mission.parent_id != parent_id:
        raise HTTPException(status_code=403, detail="Permissão negada.")
    return mission_repo.update_mission(db, mission_id, updated_data)

#Excluir missão (somente Parent)
def delete_mission(db: Session, mission_id: int, parent_id: int):
    mission = mission_repo.get_mission_by_id(db, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Missão não encontrada.")
    if mission.parent_id != parent_id:
        raise HTTPException(status_code=403, detail="Permissão negada.")
    return mission_repo.delete_mission(db, mission_id)

#Catálogo de missões (para o Kid)
def get_available_missions(db: Session, kid_id: int):
    all_missions = mission_repo.get_all_missions(db)
    completed_ids = [
        km.mission_id for km in kid_mission_repo.get_kid_missions_by_kid(db, kid_id)
    ]
    return [m for m in all_missions if m.id not in completed_ids]
