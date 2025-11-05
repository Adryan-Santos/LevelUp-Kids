from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.mission import MissionCreate, MissionOut
from app.repositories import mission as repo

router = APIRouter(prefix="/v1/missions", tags=["missions"])

@router.post("/", response_model=MissionOut, status_code=status.HTTP_201_CREATED)
def create_mission(payload: MissionCreate, db: Session = Depends(get_db)):
    return repo.create_mission(db, payload)

@router.get("/", response_model=list[MissionOut])
def list_missions(parent_id: int | None = Query(None), db: Session = Depends(get_db)):
    if parent_id is not None:
        return repo.get_missions_by_parent(db, parent_id)
    return repo.get_all_missions(db)

@router.get("/{mission_id}", response_model=MissionOut)
def get_mission_by_id(mission_id: int, db: Session = Depends(get_db)):
    mission = repo.get_mission_by_id(db, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Missão não encontrada.")
    return mission

@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    ok = repo.delete_mission(db, mission_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Missão não encontrada.")
