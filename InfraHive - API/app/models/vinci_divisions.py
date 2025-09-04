from typing import List, Optional
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class VinciDivision(Base):
    __tablename__ = 'vinci_division'
    __table_args__ = {'schema': 'dbo'}
 
    id_vinci_division: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    division_name: Mapped[str | None] = mapped_column(String(255))
    division_code: Mapped[str | None] = mapped_column(String(255))
 
    cloud_subscription: Mapped[List["CloudSubscription"]] = relationship(back_populates="vinci_division")
    servers: Mapped[List["Server"]] = relationship(back_populates="vinci_division")
    networks: Mapped[List["Network"]] = relationship(back_populates="vinci_division")