from typing import List, Optional
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class OperatingSystem(Base):
    __tablename__ = 'operating_system'
    __table_args__ = {'schema': 'dbo'}
 
    id_Operating_System: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    os_name: Mapped[str | None] = mapped_column(String(75))
    os_description: Mapped[str | None] = mapped_column(String(255))