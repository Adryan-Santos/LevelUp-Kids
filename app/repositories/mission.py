from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.mission import Mission
from app.models.parent import Parent
from app.schemas.mission import MissionCreate

# CREATE
def create_mission(db: Session, mission_data: MissionCreate) -> Mission:
    parent = db.get(Parent, mission_data.parent_id)
    if not parent:
        raise HTTPException(status_code=400, detail="Responsável não encontrado.")

    mission = Mission(**mission_data.model_dump())
    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission

# READ
def get_all_missions(db: Session) -> list[Mission]:
    return db.query(Mission).order_by(Mission.id).all()

def get_mission_by_id(db: Session, mission_id: int) -> Mission | None:
    return db.get(Mission, mission_id)

def get_missions_by_parent(db: Session, parent_id: int) -> list[Mission]:
    return db.query(Mission).filter(Mission.parent_id == parent_id).order_by(Mission.id).all()

def get_missions_by_parent(db: Session, parent_id: int):
    return db.query(Mission).filter(Mission.parent_id == parent_id).order_by(Mission.id).all()

# UPDATE
def update_mission(db: Session, mission_id: int, updated_data: dict) -> Mission | None:
    mission = get_mission_by_id(db, mission_id)
    if not mission:
        return None

    for key, value in updated_data.items():
        if hasattr(mission, key):
            setattr(mission, key, value)

    db.commit()
    db.refresh(mission)
    return mission

# DELETE
def delete_mission(db: Session, mission_id: int) -> bool:
    mission = get_mission_by_id(db, mission_id)
    if not mission:
        return False

    db.delete(mission)
    db.commit()
    return True
