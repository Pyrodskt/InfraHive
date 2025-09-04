from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud.vinci_divisions import VinciDivisionService
from app.schemas.vinci_divisions import VinciDivisionCreate, VinciDivisionUpdate, VinciDivisionResponse
from app.schemas.detailled import VinciDivisionResponseDetailled
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[VinciDivisionResponse], status_code=status.HTTP_200_OK, name="Get Vinci Divisions")
def get_divisions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    divisions = VinciDivisionService(db).get_vinci_divisions(skip=skip, limit=limit)
    if not divisions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vinci Divisions not found")
    return divisions

@router.get("/{division_id}", response_model=VinciDivisionResponse, status_code=status.HTTP_200_OK, name="Get Vinci Division")
def get_division(division_id: int, db: Session = Depends(get_db)):
    try:
        division = VinciDivisionService(db).get_vinci_division(division_id)
        return division
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/{division_id}/detailled", response_model=VinciDivisionResponseDetailled, status_code=status.HTTP_200_OK, name="Get Vinci Division")
def get_division_detailled(division_id: int, db: Session = Depends(get_db)):
    try:
        division = VinciDivisionService(db).get_vinci_division_detailled(division_id)
        return division
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=VinciDivisionResponse, status_code=status.HTTP_201_CREATED, name="Create Vinci Division")
def create_division(division: VinciDivisionCreate, db: Session = Depends(get_db)):
    try:
        result = VinciDivisionService(db).create_vinci_division(division)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{division_id}", response_model=VinciDivisionResponse, status_code=status.HTTP_200_OK, name="Update Vinci Division")
def update_division(division_id: int, division: VinciDivisionUpdate, db: Session = Depends(get_db)):
    try:
        result = VinciDivisionService(db).update_vinci_division(division_id, division)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error updating Vinci Division")

@router.delete("/{division_id}", status_code=status.HTTP_204_NO_CONTENT, name="Delete Vinci Division")
def delete_division(division_id: int, db: Session = Depends(get_db)):
    try:
        VinciDivisionService(db).delete_vinci_division(division_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error deleting Vinci Division")