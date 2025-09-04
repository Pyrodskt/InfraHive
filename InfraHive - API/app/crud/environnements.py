from sqlalchemy.orm import Session
from app.models.all import Environnement
from app.schemas.environnements import EnvironnementCreate, EnvironnementUpdate, EnvironnementResponse
from typing import List

class EnvironnementService:
    def __init__(self, db: Session):
        self.db = db

    def get_environnement(self, env_id: int) -> EnvironnementResponse:
        environnement = self.db.query(Environnement).filter(Environnement.id_environnement == env_id).first()
        if not environnement:
            raise ValueError("Environnement not found")
        return EnvironnementResponse.from_orm(environnement)

    def get_environnements(self, skip: int = 0, limit: int = 100) -> List[EnvironnementResponse]:
        environnements = self.db.query(Environnement).offset(skip).limit(limit).all()
        return [EnvironnementResponse.from_orm(env) for env in environnements]

    def create_environnement(self, env: EnvironnementCreate) -> EnvironnementResponse:
        new_env = Environnement(**env.model_dump())
        self.db.add(new_env)
        self.db.commit()
        self.db.refresh(new_env)
        return EnvironnementResponse.from_orm(new_env)

    def update_environnement(self, env_id: int, env: EnvironnementUpdate) -> EnvironnementResponse:
        existing_env = self.db.query(Environnement).filter(Environnement.id_environnement == env_id).first()
        if not existing_env:
            raise ValueError("Environnement not found")
        for key, value in env.model_dump(exclude_unset=True).items():
            setattr(existing_env, key, value)
        self.db.commit()
        self.db.refresh(existing_env)
        return EnvironnementResponse.from_orm(existing_env)

    def delete_environnement(self, env_id: int):
        existing_env = self.db.query(Environnement).filter(Environnement.id_environnement == env_id).first()
        if not existing_env:
            raise ValueError("Environnement not found")
        self.db.delete(existing_env)
        self.db.commit()
        return None