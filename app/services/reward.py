from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import reward as reward_repo

# Criar recompensa (somente Parent)
def create_reward(db: Session, data):
    if data.gold < 1:
        raise HTTPException(status_code=400, detail="Preço mínimo é 1 gold.")
    return reward_repo.create_reward(db, data)

# Editar recompensa (somente Parent)
def update_reward(db: Session, reward_id: int, updated_data: dict, parent_id: int):
    reward = reward_repo.get_reward_by_id(db, reward_id)
    if not reward:
        raise HTTPException(status_code=404, detail="Recompensa não encontrada.")
    if reward.parent_id != parent_id:
        raise HTTPException(status_code=403, detail="Permissão negada.")
    return reward_repo.update_reward(db, reward_id, updated_data)

# Excluir recompensa (somente Parent)
def delete_reward(db: Session, reward_id: int, parent_id: int):
    reward = reward_repo.get_reward_by_id(db, reward_id)
    if not reward:
        raise HTTPException(status_code=404, detail="Recompensa não encontrada.")
    if reward.parent_id != parent_id:
        raise HTTPException(status_code=403, detail="Permissão negada.")
    return reward_repo.delete_reward(db, reward_id)

# Loja (lista de recompensas disponíveis para os filhos)
def get_rewards_store(db: Session, parent_id: int):
    return reward_repo.get_rewards_by_parent(db, parent_id)
