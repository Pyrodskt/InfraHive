from typing import List, Optional
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Environnement(Base):
    __tablename__ = 'environnement'
    __table_args__ = {'schema': 'dbo'}
 
    id_environnement: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    env_name: Mapped[str | None] = mapped_column(String(45))
    env_code: Mapped[str | None] = mapped_column(String(45))
 
    cloud_subscription: Mapped[List["CloudSubscription"]] = relationship(back_populates="environnement")
    servers: Mapped[List["Server"]] = relationship(back_populates="environnement")