from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.parent import Parent
from app.schemas.parent import ParentCreate

#CREATE
def create_parent(db: Session, parent_data: ParentCreate) -> Parent:
    # Verifica se o e-mail já existe
    existing = db.query(Parent).filter(Parent.email == parent_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    parent = Parent(**parent_data.model_dump())
    db.add(parent)
    db.commit()
    db.refresh(parent)
    return parent

#READ
def get_all_parents(db: Session) -> list[Parent]:
    return db.query(Parent).order_by(Parent.id).all()

#READ ID
def get_parent_by_id(db: Session, parent_id: int) -> Parent | None:
    return db.get(Parent, parent_id)

#READ e-mail
def get_parent_by_email(db: Session, email: str) -> Parent | None:
    return db.query(Parent).filter(Parent.email == email).first()

#UPDATE
def update_parent(db: Session, parent_id: int, updated_data: dict) -> Parent | None:
    parent = get_parent_by_id(db, parent_id)
    if not parent:
        return None

    for key, value in updated_data.items():
        if hasattr(parent, key):
            setattr(parent, key, value)

    db.commit()
    db.refresh(parent)
    return parent

#DELETE
def delete_parent(db: Session, parent_id: int) -> bool:
    parent = get_parent_by_id(db, parent_id)
    if not parent:
        return False

    db.delete(parent)
    db.commit()
    return True
