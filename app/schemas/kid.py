from pydantic import BaseModel

class KidBase(BaseModel):
    nome: str
    idade: int

class KidCreate(KidBase):
    parent_id: int

class KidOut(KidBase):
    id: int
    xp: int
    gold: int
    class Config:
        orm_mode = True
