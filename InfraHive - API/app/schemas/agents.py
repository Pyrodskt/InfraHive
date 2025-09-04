from pydantic import BaseModel
from typing import Optional, List

class AgentsBase(BaseModel):
    agent_name: Optional[str] = None
    agent_process_name: Optional[str] = None
    agent_type: Optional[str] = None
    agent_criticity: Optional[str] = None
    has_api: Optional[bool] = None

class AgentsCreate(AgentsBase):
    agent_name: str
    agent_process_name: str
    agent_type: str
    agent_criticity: str
    has_api: bool

class AgentsUpdate(AgentsBase):
    pass

class AgentsResponse(AgentsBase):
    id_agent: int

    class Config:
        from_attributes = True