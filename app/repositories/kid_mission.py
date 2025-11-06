from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.kid_mission import KidMission
from app.models.kid import Kid
from app.models.mission import Mission
from app.schemas.kid_mission import KidMissionCreate

# CREATE
def create_kid_mission(db: Session, data: KidMissionCreate) -> KidMission:
    kid = db.get(Kid, data.kid_id)
    mission = db.get(Mission, data.mission_id)

    if not kid:
        raise HTTPException(status_code=404, detail="Herói não encontrado.")
    if not mission:
        raise HTTPException(status_code=404, detail="Missão não encontrada.")

    # Evita duplicação de missão para o mesmo herói
    existing = (
        db.query(KidMission)
        .filter(KidMission.kid_id == data.kid_id, KidMission.mission_id == data.mission_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Essa missão já foi registrada para esse herói.")

    kid_mission = KidMission(**data.model_dump())
    db.add(kid_mission)

    # Atualiza XP e Gold caso a missão já venha concluída
    if data.completed:
        kid.xp += mission.xp
        kid.gold += 10  # Valor fixo opcional (pode ser ajustado futuramente)

    db.commit()
    db.refresh(kid_mission)
    return kid_mission

# READ
def get_all_kid_missions(db: Session) -> list[KidMission]:
    return db.query(KidMission).order_by(KidMission.id).all()

# READ por ID
def get_kid_mission_by_id(db: Session, kid_mission_id: int) -> KidMission | None:
    return db.get(KidMission, kid_mission_id)

# READ por Kid
def get_kid_missions_by_kid(db: Session, kid_id: int) -> list[KidMission]:
    return db.query(KidMission).filter(KidMission.kid_id == kid_id).order_by(KidMission.id).all()

# DELETE
def delete_kid_mission(db: Session, kid_mission_id: int) -> bool:
    kid_mission = get_kid_mission_by_id(db, kid_mission_id)
    if not kid_mission:
        return False

    db.delete(kid_mission)
    db.commit()
    return True
