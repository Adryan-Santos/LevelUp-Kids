from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.reward import Reward
from app.models.parent import Parent
from app.schemas.reward import RewardCreate

#CREATE
def create_reward(db: Session, reward_data: RewardCreate) -> Reward:
    parent = db.get(Parent, reward_data.parent_id)
    if not parent:
        raise HTTPException(status_code=400, detail="Responsável não encontrado.")

    reward = Reward(**reward_data.model_dump())
    db.add(reward)
    db.commit()
    db.refresh(reward)
    return reward

#READ
def get_all_rewards(db: Session) -> list[Reward]:
    return db.query(Reward).order_by(Reward.id).all()

#READ ID
def get_reward_by_id(db: Session, reward_id: int) -> Reward | None:
    return db.get(Reward, reward_id)

#READ parent_ID
def get_rewards_by_parent(db: Session, parent_id: int) -> list[Reward]:
    return db.query(Reward).filter(Reward.parent_id == parent_id).order_by(Reward.id).all()

#UPDATE
def update_reward(db: Session, reward_id: int, updated_data: dict) -> Reward | None:
    reward = get_reward_by_id(db, reward_id)
    if not reward:
        return None

    for key, value in updated_data.items():
        if hasattr(reward, key):
            setattr(reward, key, value)
    db.commit()
    db.refresh(reward)
    return reward

#DELETE
def delete_reward(db: Session, reward_id: int) -> bool:
    reward = get_reward_by_id(db, reward_id)
    if not reward:
        return False

    db.delete(reward)
    db.commit()
    return True
