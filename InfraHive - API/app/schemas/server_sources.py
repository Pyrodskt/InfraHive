from pydantic import BaseModel
from typing import Optional, List

class ServerSourceBase(BaseModel):
    source_name: Optional[str] = None
    source_description: Optional[str] = None

class ServerSourceCreate(ServerSourceBase):
    source_name: str
    source_description: Optional[str] = None

class ServerSourceUpdate(ServerSourceBase):
    pass

class ServerSourceResponse(ServerSourceBase):
    id_source: int

    class Config:
        from_attributes = True