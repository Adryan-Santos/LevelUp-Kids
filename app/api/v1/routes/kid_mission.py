from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.kid_mission import KidMissionCreate, KidMissionOut
from app.repositories import kid_mission as repo

router = APIRouter(prefix="/v1/kid-missions", tags=["KidMission"])

@router.post("/", response_model=KidMissionOut, status_code=status.HTTP_201_CREATED)
def assign_mission(payload: KidMissionCreate, db: Session = Depends(get_db)):
    return repo.create_kid_mission(db, payload)

@router.get("/", response_model=list[KidMissionOut])
def list_kid_missions(db: Session = Depends(get_db)):
    return repo.get_all_kid_missions(db)
