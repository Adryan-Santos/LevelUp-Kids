from pydantic import BaseModel


class KidBase(BaseModel):
    name: str
    age: int
    level: int | None = 1
    xp: int | None = 0
    gold: int | None = 0
    avatar: str | None = None


class KidCreate(KidBase):
    parent_id: int


class KidOut(KidBase):
    id: int
    parent_id: int

    class Config:
        from_attributes = True

class KidUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    level: int | None = None
    xp: int | None = None
    gold: int | None = None
    avatar: str | None = None
