from typing import List, Optional
from sqlalchemy import String, Integer, Boolean, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from .base import Base

class Server(Base):
    __tablename__ = 'server'
    __table_args__ = {'schema': 'dbo'}
 
    id_server: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    server_name: Mapped[str | None] = mapped_column(String(255))
    is_appliance: Mapped[bool | None] = mapped_column(Boolean)
    is_obsolete: Mapped[bool | None] = mapped_column(Boolean)
    power_state: Mapped[str | None] = mapped_column(String(50))
    r7_risk_score: Mapped[str | None] = mapped_column(String(45))
   
    id_operating_system: Mapped[int] = mapped_column(ForeignKey('dbo.operating_system.id_Operating_System'))
    id_application: Mapped[int] = mapped_column(ForeignKey('dbo.application.id_application'))
    id_server_role: Mapped[int] = mapped_column(ForeignKey('dbo.server_role.id_server_role'))
    id_tier: Mapped[int] = mapped_column(ForeignKey('dbo.server_tier.id_tier'))
    id_source: Mapped[int] = mapped_column(ForeignKey('dbo.server_source.id_source'))
    id_cloud_subscription: Mapped[int | None] = mapped_column(ForeignKey('dbo.cloud_subscription.id_cloud_subscription'))
    id_environnement: Mapped[int] = mapped_column(ForeignKey('dbo.environnement.id_environnement'))
    id_vinci_division: Mapped[int] = mapped_column(ForeignKey('dbo.vinci_division.id_vinci_division'))
    update_date: Mapped[datetime.date | None] = mapped_column(Date, default=datetime.date.today)
 
    operating_system: Mapped["OperatingSystem"] = relationship(back_populates="servers")
    application: Mapped["Application"] = relationship(back_populates="servers")
    server_role: Mapped["ServerRole"] = relationship(back_populates="servers")
    server_tier: Mapped["ServerTier"] = relationship(back_populates="servers")
    server_source: Mapped["ServerSource"] = relationship(back_populates="servers")
    cloud_subscription: Mapped["CloudSubscription"] = relationship(back_populates="servers")
    environnement: Mapped["Environnement"] = relationship(back_populates="servers")
    vinci_division: Mapped["VinciDivision"] = relationship(back_populates="servers")
 
    agents: Mapped[List["ServerHasAgent"]] = relationship(back_populates="server")
    networks: Mapped[List["ServerHasNetwork"]] = relationship(back_populates="server")
    patchings: Mapped[List["Patching"]] = relationship(back_populates="server")