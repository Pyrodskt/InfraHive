from typing import List, Optional
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class ServerRole(Base):
    __tablename__ = 'server_role'
    __table_args__ = {'schema': 'dbo'}
 
    id_server_role: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_code: Mapped[str | None] = mapped_column(String(45))
    role_description: Mapped[str | None] = mapped_column(String(100))
 
    servers: Mapped[List["Server"]] = relationship(back_populates="server_role")
    