from typing import List, Optional
from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Network(Base):
    __tablename__ = 'network'
    __table_args__ = {'schema': 'dbo'}
 
    id_network: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subnet_name: Mapped[str | None] = mapped_column(String(255))
    vnet_name: Mapped[str | None] = mapped_column(String(255))
    is_dmz: Mapped[bool | None] = mapped_column(Boolean)
    id_vinci_division: Mapped[int] = mapped_column(ForeignKey('dbo.vinci_division.id_vinci_division'))
 
    vinci_division: Mapped["VinciDivision"] = relationship(back_populates="networks")
    servers: Mapped[List["ServerHasNetwork"]] = relationship(back_populates="network")