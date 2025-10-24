from pydantic import BaseModel, ConfigDict, EmailStr

class KidCreate(BaseModel):
    name: str
    age: int
    parent_id: int

class KidOut(BaseModel):
    id: int
    name: str
    age: int
    level: int
    xp: int
    gold: int
    parent_id: int
    model_config = ConfigDict(from_attributes=True)