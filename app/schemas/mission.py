from pydantic import BaseModel, ConfigDict

class MissionCreate(BaseModel):
    name: str
    descr: str
    xp_reward: int
    gold_reward: int
    parent_id: int

class MissionOut(BaseModel):
    id: int
    name: str
    descr: str
    xp_reward: int
    gold_reward: int
    parent_id: int
    model_config = ConfigDict(from_attributes=True)
