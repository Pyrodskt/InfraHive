from typing import List, Optional
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Agents(Base):
    __tablename__ = 'agents'
    __table_args__ = {'schema': 'dbo'}
 
    id_agent: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    agent_name: Mapped[str | None] = mapped_column(String(45))
    agent_process_name: Mapped[str | None] = mapped_column(String(255))
    agent_type: Mapped[str | None] = mapped_column(String(45))
    agent_criticity: Mapped[str | None] = mapped_column(String(45))
    has_api: Mapped[bool | None] = mapped_column(Boolean)
 
    servers: Mapped[List["ServerHasAgent"]] = relationship(back_populates="agent")