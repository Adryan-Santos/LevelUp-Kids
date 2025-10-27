from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Kid(Base):
    __tablename__ = "kids"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    gold = Column(Integer, default=0)

    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False)
    parent = relationship("Parent", back_populates="kids")
    kid_missions = relationship("KidMission", back_populates="kid", cascade="all, delete-orphan")
    kid_rewards  = relationship("KidReward",  back_populates="kid", cascade="all, delete-orphan")
