from typing import List, Optional
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class ServerHasNetwork(Base):
    __tablename__ = 'server_has_network'
    __table_args__ = {'schema': 'dbo'}
 
    id_server_has_network: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ip_address: Mapped[str | None] = mapped_column(String(255))
    id_network: Mapped[int] = mapped_column(ForeignKey('dbo.network.id_network'))
    id_server: Mapped[int] = mapped_column(ForeignKey('dbo.server.id_server'))
 
    network: Mapped["Network"] = relationship(back_populates="servers")
    server: Mapped["Server"] = relationship(back_populates="networks")