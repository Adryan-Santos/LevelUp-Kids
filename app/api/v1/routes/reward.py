from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.reward import RewardCreate, RewardOut
from app.repositories import reward as repo

router = APIRouter(prefix="/v1/rewards", tags=["Recompensas"])

# Criar nova recompensa
@router.post("/", response_model=RewardOut, status_code=201)
def create_reward(payload: RewardCreate, db: Session = Depends(get_db)):
    return repo.create_reward(db, payload)

# Listar todas as recompensas
@router.get("/", response_model=list[RewardOut])
def list_rewards(db: Session = Depends(get_db)):
    return repo.get_all_rewards(db)

# Buscar recompensa por ID
@router.get("/{reward_id}", response_model=RewardOut)
def get_reward(reward_id: int, db: Session = Depends(get_db)):
    reward = repo.get_reward_by_id(db, reward_id)
    if not reward:
        raise HTTPException(status_code=404, detail="Recompensa não encontrada.")
    return reward

# Atualizar recompensa
@router.put("/{reward_id}", response_model=RewardOut)
def update_reward(reward_id: int, payload: dict, db: Session = Depends(get_db)):
    updated = repo.update_reward(db, reward_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Recompensa não encontrada.")
    return updated

# Deletar recompensa
@router.delete("/{reward_id}", status_code=204)
def delete_reward(reward_id: int, db: Session = Depends(get_db)):
    if not repo.delete_reward(db, reward_id):
        raise HTTPException(status_code=404, detail="Recompensa não encontrada.")
