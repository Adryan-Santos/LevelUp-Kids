from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.reward import RewardCreate, RewardOut
from app.repositories import reward as repo

router = APIRouter(prefix="/v1/rewards", tags=["rewards"])

@router.post("/", response_model=RewardOut, status_code=status.HTTP_201_CREATED)
def create_reward(payload: RewardCreate, db: Session = Depends(get_db)):
    return repo.create_reward(db, payload)

@router.get("/", response_model=list[RewardOut])
def list_rewards(parent_id: int | None = Query(None), db: Session = Depends(get_db)):
    if parent_id is not None:
        return repo.get_rewards_by_parent(db, parent_id)
    return repo.get_all_rewards(db)

@router.get("/{reward_id}", response_model=RewardOut)
def get_reward_by_id(reward_id: int, db: Session = Depends(get_db)):
    reward = repo.get_reward_by_id(db, reward_id)
    if not reward:
        raise HTTPException(status_code=404, detail="Recompensa não encontrada.")
    return reward

@router.delete("/{reward_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reward(reward_id: int, db: Session = Depends(get_db)):
    ok = repo.delete_reward(db, reward_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Recompensa não encontrada.")
