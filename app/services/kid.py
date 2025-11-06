from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import kid as kid_repo
from app.schemas.kid import KidCreate

# Criar novo filho
def register_kid(db: Session, data: KidCreate):
    return kid_repo.create_kid(db, data)

# Atualiza XP e Level automaticamente
def add_experience(db: Session, kid_id: int, xp_gain: int, gold_gain: int = 0):
    kid = kid_repo.get_kid_by_id(db, kid_id)
    if not kid:
        raise HTTPException(status_code=404, detail="Herói não encontrado.")

    kid.xp += xp_gain
    kid.gold += gold_gain

    # A cada 100 XP → +1 level
    while kid.xp >= 100:
        kid.level += 1
        kid.xp -= 100

    # Impede gold negativo
    if kid.gold < 0:
        kid.gold = 0

    db.commit()
    db.refresh(kid)
    return kid

# Listar filhos por responsável
def list_kids_by_parent(db: Session, parent_id: int):
    return kid_repo.get_kids_by_parent(db, parent_id)
