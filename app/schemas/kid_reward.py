from pydantic import BaseModel, ConfigDict

class KidRewardCreate(BaseModel):
    kid_id: int
    reward_id: int
    purchased: bool = False

class KidRewardOut(BaseModel):
    id: int
    kid_id: int
    reward_id: int
    purchased: bool
    model_config = ConfigDict(from_attributes=True)
