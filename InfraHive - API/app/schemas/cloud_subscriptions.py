from pydantic import BaseModel
from typing import Optional, List
import datetime

class CloudSubscriptionBase(BaseModel):
    sub_name: Optional[str] = None
    sub_id: Optional[str] = None
    rg_name: Optional[str] = None
    id_source: Optional[int] = None
    id_vinci_division: Optional[int] = None
    id_environnement: Optional[int] = None
    id_tier: Optional[int] = None
    update_date: Optional[datetime.date] = None

class CloudSubscriptionCreate(BaseModel):
    sub_name: str
    sub_id: str
    rg_name: str
    id_source: int
    id_vinci_division: int
    id_environnement: int
    id_tier: int
    update_date: Optional[datetime.date] = datetime.date.today()

class CloudSubscriptionUpdate(CloudSubscriptionBase):
    pass

class CloudSubscriptionResponse(CloudSubscriptionBase):
    id_cloud_subscription: int

    class Config:
        from_attributes = True