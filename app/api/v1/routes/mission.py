from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.mission import MissionCreate, MissionOut
from app.repositories import mission as mission_repo

router = APIRouter(prefix="/v1/missions", tags=["Missões"])

# Criar nova missão
@router.post("/", response_model=MissionOut, status_code=201)
def create_mission(payload: MissionCreate, db: Session = Depends(get_db)):
    return mission_repo.create_mission(db, payload)

# Listar todas as missões
@router.get("/", response_model=list[MissionOut])
def list_missions(db: Session = Depends(get_db)):
    return mission_repo.get_all_missions(db)

# Buscar missão por ID
@router.get("/{mission_id}", response_model=MissionOut)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = mission_repo.get_mission_by_id(db, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Missão não encontrada.")
    return mission

# 🔹 NOVO: Listar todas as missões de um pai específico
@router.get("/parent/{parent_id}", response_model=list[MissionOut])
def get_missions_by_parent(parent_id: int, db: Session = Depends(get_db)):
    missions = mission_repo.get_missions_by_parent(db, parent_id)
    if not missions:
        raise HTTPException(status_code=404, detail="Nenhuma missão encontrada para este responsável.")
    return missions
