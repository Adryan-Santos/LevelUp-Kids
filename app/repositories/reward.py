from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.reward import Reward
from app.models.parent import Parent
from app.schemas.reward import RewardCreate

# CREATE (inserir nova recompensa)
def create_reward(db: Session, reward_data: RewardCreate) -> Reward:
    parent = db.get(Parent, reward_data.parent_id)
    if not parent:
        raise HTTPException(status_code=400, detail="Responsável não encontrado.")

    reward = Reward(
        title=reward_data.title,
        gold=reward_data.gold,
        parent_id=reward_data.parent_id
    )

    db.add(reward)
    db.commit()
    db.refresh(reward)
    return reward


# READ (listar todas as recompensas)
def get_all_rewards(db: Session) -> list[Reward]:
    return db.query(Reward).order_by(Reward.id).all()


# READ (buscar por ID)
def get_reward_by_id(db: Session, reward_id: int) -> Reward | None:
    return db.get(Reward, reward_id)


# READ (buscar por parent_id)
def get_rewards_by_parent(db: Session, parent_id: int) -> list[Reward]:
    return (
        db.query(Reward)
        .filter(Reward.parent_id == parent_id)
        .order_by(Reward.id)
        .all()
    )


# UPDATE (editar recompensa)
def update_reward(db: Session, reward_id: int, updated_data: dict) -> Reward | None:
    reward = get_reward_by_id(db, reward_id)
    if not reward:
        return None

    allowed = {"title", "gold"}
    for key, value in updated_data.items():
        if key in allowed:
            setattr(reward, key, value)

    db.commit()
    db.refresh(reward)
    return reward


# DELETE (remover recompensa)
def delete_reward(db: Session, reward_id: int) -> bool:
    reward = get_reward_by_id(db, reward_id)
    if not reward:
        return False

    db.delete(reward)
    db.commit()
    return True
