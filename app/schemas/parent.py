from pydantic import BaseModel, EmailStr

class ParentBase(BaseModel):
    name: str
    email: EmailStr

class ParentCreate(ParentBase):
    senha: str

class ParentLogin(BaseModel):
    email: EmailStr
    senha: str

class ParentOut(ParentBase):
    id: int
    class Config:
        orm_mode = True
