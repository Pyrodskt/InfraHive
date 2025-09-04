from typing import List, Optional
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class ServerHasAgent(Base):
    __tablename__ = 'server_has_agent'
    __table_args__ = {'schema': 'dbo'}
 
    id_server_has_agent: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: Mapped[bool | None] = mapped_column(Boolean)
    is_installable: Mapped[bool | None] = mapped_column(Boolean)
    is_required: Mapped[bool | None] = mapped_column(Boolean)
    comment: Mapped[str | None] = mapped_column(String(255))
    update_date: Mapped[datetime.date | None] = mapped_column(Date, default=datetime.date.today)
   
    id_server: Mapped[int] = mapped_column(ForeignKey('dbo.server.id_server'))
    id_agent: Mapped[int] = mapped_column(ForeignKey('dbo.agents.id_agent'))
 
    server: Mapped["Server"] = relationship(back_populates="agents")
    agent: Mapped["Agents"] = relationship(back_populates="servers")