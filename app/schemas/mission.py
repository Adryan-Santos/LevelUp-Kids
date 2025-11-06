from pydantic import BaseModel, ConfigDict

class MissionCreate(BaseModel):
    title: str
    description: str | None = None
    xp: int = 10
    gold: int = 0
    parent_id: int

class MissionOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    xp: int
    gold: int
    parent_id: int
    model_config = ConfigDict(from_attributes=True)