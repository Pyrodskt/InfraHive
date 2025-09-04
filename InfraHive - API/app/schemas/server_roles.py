from pydantic import BaseModel
from typing import Optional

class ServerRoleBase(BaseModel):
    role_code: Optional[str] = None
    role_description: Optional[str] = None

class ServerRoleCreate(ServerRoleBase):
    role_code: str

class ServerRoleUpdate(ServerRoleBase):
    pass

class ServerRoleResponse(ServerRoleBase):
    id_server_role: int

    class Config:
        from_attributes = True