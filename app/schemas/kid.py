from pydantic import BaseModel

class KidBase(BaseModel):
    name: str
    age: int
    level: int | None = 1
    xp: int | None = 0
    gold: int | None = 0

class KidCreate(KidBase):
    parent_id: int

class KidOut(KidBase):
    id: int
    parent_id: int

    class Config:
        from_attributes = True  # substitui orm_mode no Pydantic v2
