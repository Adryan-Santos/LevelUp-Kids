from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    gold = Column(Integer, default=50)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False)

    parent = relationship("Parent", back_populates="rewards")
    kid_rewards = relationship("KidReward", back_populates="reward", cascade="all, delete-orphan")
