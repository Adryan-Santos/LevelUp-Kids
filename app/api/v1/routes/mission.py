from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.mission import MissionCreate, MissionOut
from app.repositories import mission as repo

router = APIRouter(prefix="/v1/missions", tags=["Mission"])

@router.post("/", response_model=MissionOut, status_code=status.HTTP_201_CREATED)
def create_mission(payload: MissionCreate, db: Session = Depends(get_db)):
    return repo.create_mission(db, payload)

@router.get("/", response_model=list[MissionOut])
def list_missions(db: Session = Depends(get_db)):
    return repo.get_all_missions(db)

@router.get("/{mission_id}", response_model=MissionOut)
def get_mission_by_id(mission_id: int, db: Session = Depends(get_db)):
    mission = repo.get_mission_by_id(db, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Missão não encontrada.")
    return mission
