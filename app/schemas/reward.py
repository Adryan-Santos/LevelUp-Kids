from pydantic import BaseModel, ConfigDict

# Schema de criação (entrada)
class RewardCreate(BaseModel):
    title: str
    gold: int
    parent_id: int

# Schema de saída (resposta)
class RewardOut(BaseModel):
    id: int
    title: str
    gold: int
    parent_id: int
    model_config = ConfigDict(from_attributes=True)
