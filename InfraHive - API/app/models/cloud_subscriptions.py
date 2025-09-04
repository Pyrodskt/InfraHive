from typing import List, Optional
from sqlalchemy import String, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from .base import Base


class CloudSubscription(Base):
    __tablename__ = 'cloud_subscription'
    __table_args__ = {'schema': 'dbo'}
 
    id_cloud_subscription: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sub_name: Mapped[str | None] = mapped_column(String(100))
    sub_id: Mapped[str | None] = mapped_column(String(100))
    rg_name: Mapped[str | None] = mapped_column(String(100))
   
    id_source: Mapped[int] = mapped_column(ForeignKey('dbo.server_source.id_source'))
    id_vinci_division: Mapped[int] = mapped_column(ForeignKey('dbo.vinci_division.id_vinci_division'))
    id_environnement: Mapped[int] = mapped_column(ForeignKey('dbo.environnement.id_environnement'))
    id_tier: Mapped[int] = mapped_column(ForeignKey('dbo.server_tier.id_tier'))
    update_date: Mapped[datetime.date | None] = mapped_column(Date, default=datetime.date.today)
 
    vinci_division: Mapped["VinciDivision"] = relationship(back_populates="cloud_subscription")
    environnement: Mapped["Environnement"] = relationship(back_populates="cloud_subscription")
    server_tier: Mapped["ServerTier"] = relationship(back_populates="cloud_subscription")
    servers: Mapped[List["Server"]] = relationship(back_populates="cloud_subscription")