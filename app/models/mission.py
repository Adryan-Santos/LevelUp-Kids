from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    xp = Column(Integer, default=10)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False)

    parent = relationship("Parent", back_populates="missions")
    kid_missions = relationship("KidMission", back_populates="mission", cascade="all, delete-orphan")
