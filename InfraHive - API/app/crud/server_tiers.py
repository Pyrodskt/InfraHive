from sqlalchemy.orm import Session
from app.models.all import ServerTier
from app.schemas.server_tiers import ServerTierCreate, ServerTierUpdate, ServerTierResponse
from typing import List

class ServerTierService:
    def __init__(self, db: Session):
        self.db = db

    def get_server_tier(self, tier_id: int) -> ServerTierResponse:
        server_tier = self.db.query(ServerTier).filter(ServerTier.id_tier == tier_id).first()
        if not server_tier:
            raise ValueError("Server Tier not found")
        return ServerTierResponse.from_orm(server_tier)

    def get_server_tiers(self, skip: int = 0, limit: int = 100) -> List[ServerTierResponse]:
        server_tiers = self.db.query(ServerTier).offset(skip).limit(limit).all()
        return [ServerTierResponse.from_orm(tier) for tier in server_tiers]

    def create_server_tier(self, tier: ServerTierCreate) -> ServerTierResponse:
        new_tier = ServerTier(**tier.model_dump())
        self.db.add(new_tier)
        self.db.commit()
        self.db.refresh(new_tier)
        return ServerTierResponse.from_orm(new_tier)

    def update_server_tier(self, tier_id: int, tier: ServerTierUpdate) -> ServerTierResponse:
        existing_tier = self.db.query(ServerTier).filter(ServerTier.id_tier == tier_id).first()
        if not existing_tier:
            raise ValueError("Server Tier not found")
        for key, value in tier.model_dump(exclude_unset=True).items():
            setattr(existing_tier, key, value)
        self.db.commit()
        self.db.refresh(existing_tier)
        return ServerTierResponse.from_orm(existing_tier)

    def delete_server_tier(self, tier_id: int):
        existing_tier = self.db.query(ServerTier).filter(ServerTier.id_tier == tier_id).first()
        if not existing_tier:
            raise ValueError("Server Tier not found")
        self.db.delete(existing_tier)
        self.db.commit()
        return None