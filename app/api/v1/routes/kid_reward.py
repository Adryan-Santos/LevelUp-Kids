from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.kid_reward import KidRewardCreate, KidRewardOut
from app.repositories import kid_reward as repo

router = APIRouter(prefix="/v1/kid-rewards", tags=["KidReward"])

@router.post("/", response_model=KidRewardOut, status_code=status.HTTP_201_CREATED)
def buy_reward(payload: KidRewardCreate, db: Session = Depends(get_db)):
    return repo.create_kid_reward(db, payload)

@router.get("/", response_model=list[KidRewardOut])
def list_kid_rewards(db: Session = Depends(get_db)):
    return repo.get_all_kid_rewards(db)
