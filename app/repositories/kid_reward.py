from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.kid_reward import KidReward
from app.models.kid import Kid
from app.models.reward import Reward
from app.schemas.kid_reward import KidRewardCreate

# CREATE
def create_kid_reward(db: Session, data: KidRewardCreate) -> KidReward:
    kid = db.get(Kid, data.kid_id)
    reward = db.get(Reward, data.reward_id)

    if not kid:
        raise HTTPException(status_code=404, detail="Herói não encontrado.")
    if not reward:
        raise HTTPException(status_code=404, detail="Recompensa não encontrada.")

    # Verifica se o Kid já comprou essa recompensa
    existing = (
        db.query(KidReward)
        .filter(KidReward.kid_id == data.kid_id, KidReward.reward_id == data.reward_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Essa recompensa já foi registrada para este herói.")

    # Verifica se o Kid tem gold suficiente
    if kid.gold < reward.gold:  # 👈 ajustado (era price_gold)
        raise HTTPException(status_code=400, detail="Gold insuficiente para comprar a recompensa.")

    # Desconta o gold e marca como comprada
    kid.gold -= reward.gold  # 👈 ajustado (era price_gold)
    kid_reward = KidReward(**data.model_dump())
    kid_reward.purchased = True

    db.add(kid_reward)
    db.commit()
    db.refresh(kid_reward)
    return kid_reward

# READ
def get_all_kid_rewards(db: Session) -> list[KidReward]:
    return db.query(KidReward).order_by(KidReward.id).all()

# READ kid_ID
def get_kid_rewards_by_kid(db: Session, kid_id: int) -> list[KidReward]:
    return db.query(KidReward).filter(KidReward.kid_id == kid_id).order_by(KidReward.id).all()

# DELETE
def delete_kid_reward(db: Session, kid_reward_id: int) -> bool:
    kid_reward = db.get(KidReward, kid_reward_id)
    if not kid_reward:
        return False

    db.delete(kid_reward)
    db.commit()
    return True
