from sqlalchemy.orm import Session
from app.models.all import ServerRole
from app.schemas.server_roles import ServerRoleCreate, ServerRoleUpdate, ServerRoleResponse
from typing import List

class ServerRoleService:
    def __init__(self, db: Session):
        self.db = db

    def get_server_role(self, role_id: int) -> ServerRoleResponse:
        server_role = self.db.query(ServerRole).filter(ServerRole.id_server_role == role_id).first()
        if not server_role:
            raise ValueError("Server Role not found")
        return ServerRoleResponse.from_orm(server_role)

    def get_server_roles(self, skip: int = 0, limit: int = 100) -> List[ServerRoleResponse]:
        server_roles = self.db.query(ServerRole).offset(skip).limit(limit).all()
        return [ServerRoleResponse.from_orm(role) for role in server_roles]

    def create_server_role(self, role: ServerRoleCreate) -> ServerRoleResponse:
        new_role = ServerRole(**role.model_dump())
        self.db.add(new_role)
        self.db.commit()
        self.db.refresh(new_role)
        return ServerRoleResponse.from_orm(new_role)

    def update_server_role(self, role_id: int, role: ServerRoleUpdate) -> ServerRoleResponse:
        existing_role = self.db.query(ServerRole).filter(ServerRole.id_server_role == role_id).first()
        if not existing_role:
            raise ValueError("Server Role not found")
        for key, value in role.model_dump(exclude_unset=True).items():
            setattr(existing_role, key, value)
        self.db.commit()
        self.db.refresh(existing_role)
        return ServerRoleResponse.from_orm(existing_role)

    def delete_server_role(self, role_id: int):
        existing_role = self.db.query(ServerRole).filter(ServerRole.id_server_role == role_id).first()
        if not existing_role:
            raise ValueError("Server Role not found")
        self.db.delete(existing_role)
        self.db.commit()
        return None