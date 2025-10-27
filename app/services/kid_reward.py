from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import kid_reward as kid_reward_repo
from app.repositories import kid as kid_repo
from app.repositories import reward as reward_repo
from app.schemas.kid_reward import KidRewardCreate

#Comprar recompensa
def buy_reward(db: Session, data: KidRewardCreate):
    kid = kid_repo.get_kid_by_id(db, data.kid_id)
    reward = reward_repo.get_reward_by_id(db, data.reward_id)

    if not kid:
        raise HTTPException(status_code=404, detail="Herói não encontrado.")
    if not reward:
        raise HTTPException(status_code=404, detail="Recompensa não encontrada.")

    if kid.gold < reward.price_gold:
        raise HTTPException(status_code=400, detail="Gold insuficiente.")

    return kid_reward_repo.create_kid_reward(db, data)
