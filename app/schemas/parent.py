from pydantic import BaseModel, ConfigDict, EmailStr

class ParentCreate(BaseModel):
    name: str
    email: EmailStr
    senha: str

class ParentOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)
