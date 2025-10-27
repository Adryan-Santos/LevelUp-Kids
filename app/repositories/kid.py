from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.kid import Kid
from app.models.parent import Parent
from app.schemas.kid import KidCreate

#CREATE
def create_kid(db: Session, kid_data: KidCreate) -> Kid:
    # Verifica se o parent existe antes de criar o filho
    parent = db.get(Parent, kid_data.parent_id)
    if not parent:
        raise HTTPException(status_code=400, detail="Responsável não encontrado.")

    kid = Kid(**kid_data.model_dump())
    db.add(kid)
    db.commit()
    db.refresh(kid)
    return kid

#READ
def get_all_kids(db: Session) -> list[Kid]:
    return db.query(Kid).order_by(Kid.id).all()

#READ ID
def get_kid_by_id(db: Session, kid_id: int) -> Kid | None:
    return db.get(Kid, kid_id)

#READ parent_ID
def get_kids_by_parent(db: Session, parent_id: int) -> list[Kid]:
    return db.query(Kid).filter(Kid.parent_id == parent_id).order_by(Kid.id).all()

#UPDATE
def update_kid(db: Session, kid_id: int, updated_data: dict) -> Kid | None:
    kid = get_kid_by_id(db, kid_id)
    if not kid:
        return None

    for key, value in updated_data.items():
        if hasattr(kid, key):
            setattr(kid, key, value)

    db.commit()
    db.refresh(kid)
    return kid

#DELETE
def delete_kid(db: Session, kid_id: int) -> bool:
    kid = get_kid_by_id(db, kid_id)
    if not kid:
        return False

    db.delete(kid)
    db.commit()
    return True
