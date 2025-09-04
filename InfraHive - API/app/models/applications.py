from typing import List, Optional
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Application(Base):
    __tablename__ = 'application'
    __table_args__ = {'schema': 'dbo'}
 
    id_application: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    app_name: Mapped[str | None] = mapped_column(String(100))
    app_code: Mapped[str | None] = mapped_column(String(10))
    app_owner: Mapped[str | None] = mapped_column(String(100))
 
    servers: Mapped[List["Server"]] = relationship(back_populates="application")