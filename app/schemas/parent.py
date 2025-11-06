from pydantic import BaseModel, EmailStr, ConfigDict

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
    model_config = ConfigDict(from_attributes=True)
