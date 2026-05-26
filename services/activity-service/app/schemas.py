from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

class ActivityCreate(BaseModel):
    user_id: int
    game_id: Optional[int] = None
    action: str

class ActivityOut(BaseModel):
    id: int
    user_id: int
    game_id: Optional[int]
    action: str
    created_at: datetime
    game: Optional[Any] = None
    model_config = {"from_attributes": True}