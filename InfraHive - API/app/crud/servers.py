from sqlalchemy.orm import Session, joinedload
from app.models.all import Server
from app.schemas.servers import ServerCreate, ServerUpdate, ServerResponse
from app.schemas.detailled import ServerResponseDetailled
from typing import List

class ServerService:
    def __init__(self, db: Session):
        self.db = db

    def get_server(self, server_id: int) -> ServerResponse:
        server = self.db.query(Server).filter(Server.id_server == server_id).first()
        if not server:
            raise ValueError("Server not found")
        return ServerResponse.from_orm(server)

    def get_servers(self, skip: int = 0, limit: int = 100) -> List[ServerResponse]:
        servers = self.db.query(Server).offset(skip).limit(limit).all()
        return [ServerResponse.from_orm(server) for server in servers]

    def create_server(self, server: ServerCreate) -> ServerResponse:
        new_server = Server(**server.model_dump())
        self.db.add(new_server)
        self.db.commit()
        self.db.refresh(new_server)
        return ServerResponse.from_orm(new_server)

    def update_server(self, server_id: int, server: ServerUpdate) -> ServerResponse:
        existing_server = self.db.query(Server).filter(Server.id_server == server_id).first()
        if not existing_server:
            raise ValueError("Server not found")
        for key, value in server.model_dump(exclude_unset=True).items():
            setattr(existing_server, key, value)
        self.db.commit()
        self.db.refresh(existing_server)
        return ServerResponse.from_orm(existing_server)

    def delete_server(self, server_id: int):
        existing_server = self.db.query(Server).filter(Server.id_server == server_id).first()
        if not existing_server:
            raise ValueError("Server not found")
        self.db.delete(existing_server)
        self.db.commit()
        return None

    def get_server_detailled(self, server_id: int) -> ServerResponseDetailled:
        server = (
            self.db.query(Server)
            .options(
                joinedload(Server.application),
                joinedload(Server.cloud_subscription),
                joinedload(Server.environnement),
                joinedload(Server.operating_system),
                joinedload(Server.server_role),
                joinedload(Server.server_source),
                joinedload(Server.server_tier),
                joinedload(Server.vinci_division)
            )
            .filter(Server.id_server == server_id)
            .first()
        )
        if not server:
            raise ValueError("Server not found")
        return ServerResponseDetailled.from_orm(server)
