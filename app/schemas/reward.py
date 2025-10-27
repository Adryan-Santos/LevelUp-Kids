from pydantic import BaseModel, ConfigDict
from typing import Optional

class RewardCreate(BaseModel):
    name: str
    descr: Optional[str] = None
    price_gold: int
    parent_id: int

class RewardOut(BaseModel):
    id: int
    name: str
    descr: Optional[str] = None
    price_gold: int
    parent_id: int
    model_config = ConfigDict(from_attributes=True)
