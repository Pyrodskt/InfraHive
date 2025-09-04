import datetime
from typing import List
from sqlalchemy import (
    String, 
    Integer, 
    Boolean, 
    Date, 
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship,
    DeclarativeBase # Import de la classe de base déclarative
)


# Déclaration de la base pour les classes
# Remplace `Base = declarative_base()`
class Base(DeclarativeBase):
    pass


# Modèles générés à partir du script SQL
class OperatingSystem(Base):
    __tablename__ = 'operating_system'
    __table_args__ = {'schema': 'dbo'}

    # Utilisation de Mapped et mapped_column
    id_Operating_System: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    os_name: Mapped[str | None] = mapped_column(String(75))
    os_description: Mapped[str | None] = mapped_column(String(255))

    # Relation inverse avec annotation de type Mapped[List[...]]
    servers: Mapped[List["Server"]] = relationship(back_populates="operating_system")

    def __repr__(self):
        return f"<OperatingSystem(name='{self.os_name}')>"


class Application(Base):
    __tablename__ = 'application'
    __table_args__ = {'schema': 'dbo'}

    id_application: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    app_name: Mapped[str | None] = mapped_column(String(100))
    app_code: Mapped[str | None] = mapped_column(String(10))
    app_owner: Mapped[str | None] = mapped_column(String(100))

    servers: Mapped[List["Server"]] = relationship(back_populates="application")
    
    def __repr__(self):
        return f"<Application(name='{self.app_name}')>"


class ServerRole(Base):
    __tablename__ = 'server_role'
    __table_args__ = {'schema': 'dbo'}

    id_server_role: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_code: Mapped[str | None] = mapped_column(String(45))
    role_description: Mapped[str | None] = mapped_column(String(100))

    servers: Mapped[List["Server"]] = relationship(back_populates="server_role")

    def __repr__(self):
        return f"<ServerRole(code='{self.role_code}')>"


class ServerTier(Base):
    __tablename__ = 'server_tier'
    __table_args__ = {'schema': 'dbo'}

    id_tier: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tier_name: Mapped[str | None] = mapped_column(String(45))

    servers: Mapped[List["Server"]] = relationship(back_populates="server_tier")
    cloud_subscription: Mapped[List["CloudSubscription"]] = relationship(back_populates="server_tier")

    def __repr__(self):
        return f"<ServerTier(name='{self.tier_name}')>"


class ServerSource(Base):
    __tablename__ = 'server_source'
    __table_args__ = {'schema': 'dbo'}

    id_source: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_name: Mapped[str | None] = mapped_column(String(45))
    source_description: Mapped[str | None] = mapped_column(String(100))

    servers: Mapped[List["Server"]] = relationship(back_populates="server_source")

    def __repr__(self):
        return f"<ServerSource(name='{self.source_name}')>"


class VinciDivision(Base):
    __tablename__ = 'vinci_division'
    __table_args__ = {'schema': 'dbo'}

    id_vinci_division: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    division_name: Mapped[str | None] = mapped_column(String(255))
    division_code: Mapped[str | None] = mapped_column(String(255))

    cloud_subscription: Mapped[List["CloudSubscription"]] = relationship(back_populates="vinci_division")
    servers: Mapped[List["Server"]] = relationship(back_populates="vinci_division")
    networks: Mapped[List["Network"]] = relationship(back_populates="vinci_division")

    def __repr__(self):
        return f"<VinciDivision(name='{self.division_name}')>"


class Environnement(Base):
    __tablename__ = 'environnement'
    __table_args__ = {'schema': 'dbo'}

    id_environnement: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    env_name: Mapped[str | None] = mapped_column(String(45))
    env_code: Mapped[str | None] = mapped_column(String(45))

    cloud_subscription: Mapped[List["CloudSubscription"]] = relationship(back_populates="environnement")
    servers: Mapped[List["Server"]] = relationship(back_populates="environnement")

    def __repr__(self):
        return f"<Environnement(name='{self.env_name}')>"


class CloudSubscription(Base):
    __tablename__ = 'cloud_subscription'
    __table_args__ = {'schema': 'dbo'}

    id_cloud_subscription: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sub_name: Mapped[str | None] = mapped_column(String(100))
    sub_id: Mapped[str | None] = mapped_column(String(100))
    rg_name: Mapped[str | None] = mapped_column(String(100))
    
    # Colonnes de clé étrangère
    id_source: Mapped[int] = mapped_column(ForeignKey('dbo.server_source.id_source'))
    id_vinci_division: Mapped[int] = mapped_column(ForeignKey('dbo.vinci_division.id_vinci_division'))
    id_environnement: Mapped[int] = mapped_column(ForeignKey('dbo.environnement.id_environnement'))
    id_tier: Mapped[int] = mapped_column(ForeignKey('dbo.server_tier.id_tier'))
    update_date: Mapped[datetime.date | None] = mapped_column(Date, default=datetime.date.today)

    # Relations
    vinci_division: Mapped["VinciDivision"] = relationship(back_populates="cloud_subscription")
    environnement: Mapped["Environnement"] = relationship(back_populates="cloud_subscription")
    server_tier: Mapped["ServerTier"] = relationship(back_populates="cloud_subscription")
    servers: Mapped[List["Server"]] = relationship(back_populates="cloud_subscription")

    def __repr__(self):
        return f"<CloudSubscription(name='{self.sub_name}')>"


class Server(Base):
    __tablename__ = 'server'
    __table_args__ = {'schema': 'dbo'}

    id_server: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    server_name: Mapped[str | None] = mapped_column(String(255))
    is_appliance: Mapped[bool | None] = mapped_column(Boolean)
    is_obsolete: Mapped[bool | None] = mapped_column(Boolean)
    power_state: Mapped[str | None] = mapped_column(String(50))
    r7_risk_score: Mapped[str | None] = mapped_column(String(45))
    
    # Colonnes de clé étrangère
    id_operating_system: Mapped[int] = mapped_column(ForeignKey('dbo.operating_system.id_Operating_System'))
    id_application: Mapped[int] = mapped_column(ForeignKey('dbo.application.id_application'))
    id_server_role: Mapped[int] = mapped_column(ForeignKey('dbo.server_role.id_server_role'))
    id_tier: Mapped[int] = mapped_column(ForeignKey('dbo.server_tier.id_tier'))
    id_source: Mapped[int] = mapped_column(ForeignKey('dbo.server_source.id_source'))
    id_cloud_subscription: Mapped[int | None] = mapped_column(ForeignKey('dbo.cloud_subscription.id_cloud_subscription'))
    id_environnement: Mapped[int] = mapped_column(ForeignKey('dbo.environnement.id_environnement'))
    id_vinci_division: Mapped[int] = mapped_column(ForeignKey('dbo.vinci_division.id_vinci_division'))
    update_date: Mapped[datetime.date | None] = mapped_column(Date, default=datetime.date.today)

    # Relations corrigées pour les correspondances back_populates
    operating_system: Mapped["OperatingSystem"] = relationship(back_populates="servers")
    application: Mapped["Application"] = relationship(back_populates="servers")
    server_role: Mapped["ServerRole"] = relationship(back_populates="servers")
    server_tier: Mapped["ServerTier"] = relationship(back_populates="servers")
    server_source: Mapped["ServerSource"] = relationship(back_populates="servers")
    cloud_subscription: Mapped["CloudSubscription"] = relationship(back_populates="servers")
    environnement: Mapped["Environnement"] = relationship(back_populates="servers")
    vinci_division: Mapped["VinciDivision"] = relationship(back_populates="servers")

    # Relations pour les tables de liaison (inchangées)
    agents: Mapped[List["ServerHasAgent"]] = relationship(back_populates="server")
    networks: Mapped[List["ServerHasNetwork"]] = relationship(back_populates="server")
    patchings: Mapped[List["Patching"]] = relationship(back_populates="server")

    def __repr__(self):
        return f"<Server(name='{self.server_name}')>"


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

    def __repr__(self):
        return f"<Network(name='{self.subnet_name}')>"


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

    def __repr__(self):
        return f"<Agents(name='{self.agent_name}')>"


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

    def __repr__(self):
        return f"<ServerHasAgent(server_id={self.id_server}, agent_id={self.id_agent})>"


class UpdatePhase(Base):
    __tablename__ = 'update_phase'
    __table_args__ = {'schema': 'dbo'}

    id_update_phase: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    phase_name: Mapped[str | None] = mapped_column(String(255))
    phase_description: Mapped[str | None] = mapped_column(String(255))
    phase_next_period: Mapped[str | None] = mapped_column(String(255))

    patchings: Mapped[List["Patching"]] = relationship(back_populates="update_phase")

    def __repr__(self):
        return f"<UpdatePhase(name='{self.phase_name}')>"


class Patching(Base):
    __tablename__ = 'patching'
    __table_args__ = {'schema': 'dbo'}

    id_patching: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: Mapped[bool | None] = mapped_column(Boolean)
    id_server: Mapped[int] = mapped_column(ForeignKey('dbo.server.id_server'))
    id_update_phase: Mapped[int] = mapped_column(ForeignKey('dbo.update_phase.id_update_phase'))
    update_date: Mapped[datetime.date | None] = mapped_column(Date, default=datetime.date.today)

    server: Mapped["Server"] = relationship(back_populates="patchings")
    update_phase: Mapped["UpdatePhase"] = relationship(back_populates="patchings")

    def __repr__(self):
        return f"<Patching(server_id={self.id_server}, phase_id={self.id_update_phase})>"


class ServerHasNetwork(Base):
    __tablename__ = 'server_has_network'
    __table_args__ = {'schema': 'dbo'}

    id_server_has_network: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ip_address: Mapped[str | None] = mapped_column(String(255))
    id_network: Mapped[int] = mapped_column(ForeignKey('dbo.network.id_network'))
    id_server: Mapped[int] = mapped_column(ForeignKey('dbo.server.id_server'))

    network: Mapped["Network"] = relationship(back_populates="servers")
    server: Mapped["Server"] = relationship(back_populates="networks")

    def __repr__(self):
        return f"<ServerHasNetwork(server_id={self.id_server}, network_id={self.id_network})>"