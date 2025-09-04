from pydantic import BaseModel
from typing import Optional, List

class NetworkBase(BaseModel):
    subnet_name: Optional[str] = None
    vnet_name: Optional[str] = None
    is_dmz: Optional[bool] = None
    id_vinci_division: Optional[int] = None

class NetworkCreate(NetworkBase):
    subnet_name: str
    vnet_name: str
    is_dmz: bool
    id_vinci_division: int

class NetworkUpdate(NetworkBase):
    pass

class NetworkResponse(NetworkBase):
    id_network: int
    
    class Config:
        from_attributes = True