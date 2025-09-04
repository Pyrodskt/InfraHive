from pydantic import BaseModel
from typing import Optional, List
# from .networks import NetworkResponse
# from .cloud_subscriptions import CloudSubscriptionResponse
# from .servers import ServerResponse

class VinciDivisionBase(BaseModel):
    division_name: Optional[str] = None
    division_code: Optional[str] = None

class VinciDivisionCreate(VinciDivisionBase):
    division_name: str
    division_code: str

class VinciDivisionUpdate(VinciDivisionBase):
    pass

class VinciDivisionResponse(VinciDivisionBase):
    id_vinci_division: int

    class Config:
        from_attributes = True

# class VinciDivisionResponseDetailled(VinciDivisionBase):
#     id_vinci_division: int
#     networks: List[NetworkResponse] = []
#     cloud_subscriptions: List[CloudSubscriptionResponse] = []
#     servers: List[ServerResponse] = []

#     class Config:
#         from_attributes = True