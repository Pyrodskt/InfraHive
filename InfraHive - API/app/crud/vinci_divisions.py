from sqlalchemy.orm import Session, joinedload
from app.models.all import VinciDivision
from app.schemas.vinci_divisions import VinciDivisionCreate, VinciDivisionUpdate, VinciDivisionResponse
from app.schemas.detailled import VinciDivisionResponseDetailled
from typing import List

class VinciDivisionService:
    def __init__(self, db: Session):
        self.db = db

    def get_vinci_division(self, division_id: int) -> VinciDivisionResponse:
        division = self.db.query(VinciDivision).filter(VinciDivision.id_vinci_division == division_id).first()
        if not division:
            raise ValueError("Vinci Division not found")
        return VinciDivisionResponse.from_orm(division)

    def get_vinci_divisions(self, skip: int = 0, limit: int = 100) -> List[VinciDivisionResponse]:
        divisions = self.db.query(VinciDivision).offset(skip).limit(limit).all()
        return [VinciDivisionResponse.from_orm(division) for division in divisions]

    def create_vinci_division(self, division: VinciDivisionCreate) -> VinciDivisionResponse:
        new_division = VinciDivision(**division.model_dump())
        self.db.add(new_division)
        self.db.commit()
        self.db.refresh(new_division)
        return VinciDivisionResponse.from_orm(new_division)

    def update_vinci_division(self, division_id: int, division: VinciDivisionUpdate) -> VinciDivisionResponse:
        existing_division = self.db.query(VinciDivision).filter(VinciDivision.id_vinci_division == division_id).first()
        if not existing_division:
            raise ValueError("Vinci Division not found")
        for key, value in division.model_dump(exclude_unset=True).items():
            setattr(existing_division, key, value)
        self.db.commit()
        self.db.refresh(existing_division)
        return VinciDivisionResponse.from_orm(existing_division)

    def delete_vinci_division(self, division_id: int):
        existing_division = self.db.query(VinciDivision).filter(VinciDivision.id_vinci_division == division_id).first()
        if not existing_division:
            raise ValueError("Vinci Division not found")
        self.db.delete(existing_division)
        self.db.commit()
        return None

    def get_vinci_division_detailled(self, division_id: int) -> VinciDivisionResponseDetailled:
        division = (
            self.db.query(VinciDivision)
            .options(joinedload(VinciDivision.networks),joinedload(VinciDivision.cloud_subscription),joinedload(VinciDivision.servers))
            .filter(VinciDivision.id_vinci_division == division_id)
            .first()
        )
        if not division:
            raise ValueError("Vinci Division not found")
        return VinciDivisionResponseDetailled.from_orm(division)