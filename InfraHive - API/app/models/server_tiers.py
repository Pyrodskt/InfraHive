from typing import List, Optional
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class ServerTier(Base):
    __tablename__ = 'server_tier'
    __table_args__ = {'schema': 'dbo'}
 
    id_tier: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tier_name: Mapped[str | None] = mapped_column(String(45))
 
    servers: Mapped[List["Server"]] = relationship(back_populates="server_tier")
    cloud_subscription: Mapped[List["CloudSubscription"]] = relationship(back_populates="server_tier")