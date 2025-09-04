from sqlalchemy.orm import Session
from app.models.all import OperatingSystem
from app.schemas.operating_systems import OperatingSystemCreate, OperatingSystemUpdate, OperatingSystemResponse

class OperatingSystemService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_operating_system(self, os_id: int) -> OperatingSystemResponse:
        operating_system = self.db.query(OperatingSystem).filter(OperatingSystem.id_Operating_System == os_id).first()
        if not operating_system:
            raise ValueError("Operating System not found")
        return OperatingSystemResponse.from_orm(operating_system)

    def get_operating_systems(self, skip: int = 0, limit: int = 100) -> list[OperatingSystemResponse]:
        operating_systems = self.db.query(OperatingSystem).order_by(OperatingSystem.id_Operating_System).offset(skip).limit(limit).all()
        return [OperatingSystemResponse.from_orm(operating_system) for operating_system in operating_systems]

    def create_operating_system(self, os: OperatingSystemCreate) -> OperatingSystemResponse:
        new_os = OperatingSystem(**os.dict())
        self.db.add(new_os)
        self.db.commit()
        self.db.refresh(new_os)
        return OperatingSystemResponse.from_orm(new_os)

    def update_operating_system(self, os_id: int, os: OperatingSystemUpdate) -> OperatingSystemResponse:
        existing_os = self.db.query(OperatingSystem).filter(OperatingSystem.id_Operating_System==os_id).first()
        if not existing_os:
            raise ValueError("Operating System not found")
        for key, value in os.dict().items():
            setattr(existing_os, key, value)
        self.db.commit()
        self.db.refresh(existing_os)
        return OperatingSystemResponse.from_orm(existing_os)

    def delete_operating_system(self, os_id:int):
        existing_os = self.db.query(OperatingSystem).filter(OperatingSystem.id_Operating_System==os_id).first()
        if not existing_os:
            raise ValueError("Operating System not found")
        self.db.delete(existing_os)
        self.db.commit()
        return None

