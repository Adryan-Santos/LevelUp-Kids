from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)

    kids = relationship("Kid", back_populates="parent", cascade="all, delete-orphan")
    missions = relationship("Mission", back_populates="parent", cascade="all, delete-orphan")
    rewards = relationship("Reward", back_populates="parent", cascade="all, delete-orphan")
