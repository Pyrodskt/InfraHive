from pydantic import BaseModel
from typing import Optional, List

class EnvironnementBase(BaseModel):
    env_name: Optional[str] = None
    env_code: Optional[str] = None

class EnvironnementCreate(EnvironnementBase):
    env_name: str
    env_code: str

class EnvironnementUpdate(EnvironnementBase):
    pass

class EnvironnementResponse(EnvironnementBase):
    id_environnement: int

    class Config:
        from_attributes = True