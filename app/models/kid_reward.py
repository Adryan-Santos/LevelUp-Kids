from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class KidReward(Base):
    __tablename__ = "kid_rewards"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    kid_id = Column(Integer, ForeignKey("kids.id"), nullable=False)
    reward_id = Column(Integer, ForeignKey("rewards.id"), nullable=False)
    purchased = Column(Boolean, default=False)

    kid = relationship("Kid", back_populates="kid_rewards")
    reward = relationship("Reward", back_populates="kid_rewards")
