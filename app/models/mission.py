from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    descr = Column(String, nullable=False)
    xp_reward = Column(Integer, default=0)
    gold_reward = Column(Integer, default=0)

    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False)
    parent = relationship("Parent", back_populates="missions")
    kid_missions = relationship("KidMission", back_populates="mission")