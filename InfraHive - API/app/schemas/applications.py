from pydantic import BaseModel
from typing import Optional

class ApplicationBase(BaseModel):
    app_name: Optional[str] = None
    app_code: Optional[str] = None
    app_owner: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    app_name: str

class ApplicationUpdate(ApplicationBase):
    pass

class ApplicationResponse(ApplicationBase):
    id_application: int

    class Config:
        from_attributes = True