from pydantic import BaseModel

class OperatingSystemBase(BaseModel):
    os_name: str
    os_description: str | None = None

class OperatingSystemCreate(OperatingSystemBase):
    pass

class OperatingSystemUpdate(OperatingSystemBase):
    pass

class OperatingSystemResponse(OperatingSystemBase):
    id_Operating_System: int
    
    class Config:
        from_attributes = True