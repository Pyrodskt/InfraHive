from pydantic import BaseModel
from typing import Optional, List
import datetime

#== BASE ==
from .vinci_divisions import VinciDivisionBase
from .servers import ServerBase

#== RESPONSE ==
from .networks import NetworkResponse
from .cloud_subscriptions import CloudSubscriptionResponse
from .servers import ServerResponse
from .applications import ApplicationResponse
from .cloud_subscriptions import CloudSubscriptionResponse
from .environnements import EnvironnementResponse
from .operating_systems import OperatingSystemResponse
from .server_roles import ServerRoleResponse
from .server_sources import ServerSourceResponse
from .server_tiers import ServerTierResponse
from .vinci_divisions import VinciDivisionResponse


class VinciDivisionResponseDetailled(VinciDivisionBase):
    id_vinci_division: int
    networks: Optional[List[NetworkResponse]] = []
    cloud_subscriptions: Optional[List[CloudSubscriptionResponse]] = []
    servers: Optional[List[ServerResponse]] = []

    class Config:
        from_attributes = True

class ServerResponseDetailled(BaseModel):
    id_server: int
    server_name: Optional[str] = None
    is_appliance: Optional[bool] = None
    is_obsolete: Optional[bool] = None
    power_state: Optional[str] = None
    r7_risk_score: Optional[str] = None
    update_date: Optional[datetime.date] = None
    application: Optional[ApplicationResponse] = None
    cloud_subscription: Optional[CloudSubscriptionResponse] = None
    environnement: Optional[EnvironnementResponse] = None
    operating_system: Optional[OperatingSystemResponse] = None
    server_role: Optional[ServerRoleResponse] = None
    server_source: Optional[ServerSourceResponse] = None
    server_tier: Optional[ServerTierResponse] = None
    vinci_division: Optional[VinciDivisionResponse] = None

    class Config:
        from_attributes = True