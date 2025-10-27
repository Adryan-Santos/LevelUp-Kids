from pydantic import BaseModel, ConfigDict

class KidMissionCreate(BaseModel):
    kid_id: int
    mission_id: int
    completed: bool = False

class KidMissionOut(BaseModel):
    id: int
    kid_id: int
    mission_id: int
    completed: bool 
    model_config = ConfigDict(from_attributes=True)
