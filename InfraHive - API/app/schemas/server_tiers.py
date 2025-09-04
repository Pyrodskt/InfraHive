from pydantic import BaseModel
from typing import Optional

class ServerTierBase(BaseModel):
    tier_name: Optional[str] = None

class ServerTierCreate(ServerTierBase):
    tier_name: str

class ServerTierUpdate(ServerTierBase):
    pass

class ServerTierResponse(ServerTierBase):
    id_tier: int

    class Config:
        from_attributes = True