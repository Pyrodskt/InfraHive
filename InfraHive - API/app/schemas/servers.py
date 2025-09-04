from pydantic import BaseModel
from typing import Optional, List
import datetime
# from .applications import ApplicationResponse
# from .cloud_subscriptions import CloudSubscriptionResponse
# from .environnements import EnvironnementResponse
# from .operating_systems import OperatingSystemResponse
# from .server_roles import ServerRoleResponse
# from .server_sources import ServerSourceResponse
# from .server_tiers import ServerTierResponse
# from .vinci_divisions import VinciDivisionResponse

class ServerBase(BaseModel):
    server_name: Optional[str] = None
    is_appliance: Optional[bool] = None
    is_obsolete: Optional[bool] = None
    power_state: Optional[str] = None
    r7_risk_score: Optional[str] = None
    id_operating_system: Optional[int] = None
    id_application: Optional[int] = None
    id_server_role: Optional[int] = None
    id_tier: Optional[int] = None
    id_source: Optional[int] = None
    id_cloud_subscription: Optional[int] = None
    id_environnement: Optional[int] = None
    id_vinci_division: Optional[int] = None
    update_date: Optional[datetime.date] = None

class ServerCreate(BaseModel):
    server_name: str
    is_appliance: bool
    is_obsolete: bool
    power_state: str
    r7_risk_score: str
    id_operating_system: int
    id_application: int
    id_server_role: int
    id_tier: int
    id_source: int
    id_cloud_subscription: Optional[int] = None
    id_environnement: int
    id_vinci_division: int
    update_date: Optional[datetime.date] = datetime.date.today()

class ServerUpdate(ServerBase):
    pass

class ServerResponse(ServerBase):
    id_server: int

    class Config:
        from_attributes = True

# class ServerResponseDetailled(VinciDivisionBase):
#     id_server: int
#     application: ApplicationResponse
#     cloud_subscription: CloudSubscriptionResponse
#     environnement: EnvironnementResponse
#     operating_system: OperatingSystemResponse
#     role: ServerRoleResponse
#     source: ServerSourceResponse
#     tier: ServerTierResponse
#     vinci_division: VinciDivisionResponse

#     class Config:
#         from_attributes = True
