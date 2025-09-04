from sqlalchemy.orm import Session
from app.models.all import ServerSource
from app.schemas.server_sources import ServerSourceCreate, ServerSourceUpdate, ServerSourceResponse
from typing import List

class ServerSourceService:
    def __init__(self, db: Session):
        self.db = db

    def get_server_source(self, source_id: int) -> ServerSourceResponse:
        source = self.db.query(ServerSource).filter(ServerSource.id_source == source_id).first()
        if not source:
            raise ValueError("Server Source not found")
        return ServerSourceResponse.from_orm(source)

    def get_server_sources(self, skip: int = 0, limit: int = 100) -> List[ServerSourceResponse]:
        sources = self.db.query(ServerSource).offset(skip).limit(limit).all()
        return [ServerSourceResponse.from_orm(source) for source in sources]

    def create_server_source(self, source: ServerSourceCreate) -> ServerSourceResponse:
        new_source = ServerSource(**source.model_dump())
        self.db.add(new_source)
        self.db.commit()
        self.db.refresh(new_source)
        return ServerSourceResponse.from_orm(new_source)

    def update_server_source(self, source_id: int, source: ServerSourceUpdate) -> ServerSourceResponse:
        existing_source = self.db.query(ServerSource).filter(ServerSource.id_source == source_id).first()
        if not existing_source:
            raise ValueError("Server Source not found")
        for key, value in source.model_dump(exclude_unset=True).items():
            setattr(existing_source, key, value)
        self.db.commit()
        self.db.refresh(existing_source)
        return ServerSourceResponse.from_orm(existing_source)

    def delete_server_source(self, source_id: int):
        existing_source = self.db.query(ServerSource).filter(ServerSource.id_source == source_id).first()
        if not existing_source:
            raise ValueError("Server Source not found")
        self.db.delete(existing_source)
        self.db.commit()
        return None