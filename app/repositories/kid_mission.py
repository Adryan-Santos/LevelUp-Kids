from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.kid_mission import KidMission
from app.models.kid import Kid
from app.models.mission import Mission
from app.schemas.kid_mission import KidMissionCreate


# ===========================
# CREATE ou COMPLETAR MISSÃO
# ===========================
def create_kid_mission(db: Session, data: KidMissionCreate) -> KidMission:
    kid = db.get(Kid, data.kid_id)
    mission = db.get(Mission, data.mission_id)

    if not kid:
        raise HTTPException(404, "Herói não encontrado.")
    if not mission:
        raise HTTPException(404, "Missão não encontrada.")

    # Verifica se já existe registro
    existing = (
        db.query(KidMission)
        .filter(
            KidMission.kid_id == data.kid_id,
            KidMission.mission_id == data.mission_id
        )
        .first()
    )

    # Já existe → marcar como concluída
    if existing:
        if not existing.completed:
            existing.completed = True

            # XP + GOLD
            kid.xp += mission.xp
            kid.gold += mission.gold

            # level = xp // 100 + 1
            kid.level = max(1, kid.xp // 100 + 1)

        db.commit()
        db.refresh(existing)
        return existing

    # Senão → criar do zero
    kid_mission = KidMission(**data.model_dump())
    db.add(kid_mission)

    if data.completed:
        kid_mission.completed = True

        kid.xp += mission.xp
        kid.gold += mission.gold
        kid.level = max(1, kid.xp // 100 + 1)

    db.commit()
    db.refresh(kid_mission)
    return kid_mission


# ===========================
# LISTAR TODAS AS MISSÕES
# ===========================
def get_all_kid_missions(db: Session):
    return db.query(KidMission).all()


# ===========================
# LISTAR MISSÕES DE UM HERÓI
# ===========================
def get_kid_missions_by_kid(db: Session, kid_id: int):
    return (
        db.query(KidMission)
        .filter(KidMission.kid_id == kid_id)
        .all()
    )


# ===========================
# BUSCAR POR ID
# ===========================
def get_kid_mission_by_id(db: Session, kid_mission_id: int):
    return db.get(KidMission, kid_mission_id)


# ===========================
# DELETAR
# ===========================
def delete_kid_mission(db: Session, kid_mission_id: int) -> bool:
    km = db.get(KidMission, kid_mission_id)
    if not km:
        return False

    db.delete(km)
    db.commit()
    return True
