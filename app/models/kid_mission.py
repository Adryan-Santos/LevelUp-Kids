from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class KidMission(Base):
    __tablename__ = "kid_missions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    kid_id = Column(Integer, ForeignKey("kids.id"), nullable=False)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    completed = Column(Boolean, default=False)

    kid = relationship("Kid", back_populates="kid_missions")
    mission = relationship("Mission", back_populates="kid_missions")
