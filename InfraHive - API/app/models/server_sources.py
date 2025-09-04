from typing import List, Optional
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class ServerSource(Base):
    __tablename__ = 'server_source'
    __table_args__ = {'schema': 'dbo'}
 
    id_source: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_name: Mapped[str | None] = mapped_column(String(45))
    source_description: Mapped[str | None] = mapped_column(String(100))
 
    servers: Mapped[List["Server"]] = relationship(back_populates="server_source")