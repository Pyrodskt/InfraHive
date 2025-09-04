from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud.environnements import EnvironnementService
from app.schemas.environnements import EnvironnementCreate, EnvironnementUpdate, EnvironnementResponse
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[EnvironnementResponse], status_code=status.HTTP_200_OK, name="Get Environnements")
def get_environnements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    environnements = EnvironnementService(db).get_environnements(skip=skip, limit=limit)
    if not environnements:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Environnements not found")
    return environnements

@router.get("/{env_id}", response_model=EnvironnementResponse, status_code=status.HTTP_200_OK, name="Get Environnement")
def get_environnement(env_id: int, db: Session = Depends(get_db)):
    try:
        environnement = EnvironnementService(db).get_environnement(env_id)
        return environnement
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=EnvironnementResponse, status_code=status.HTTP_201_CREATED, name="Create Environnement")
def create_environnement(env: EnvironnementCreate, db: Session = Depends(get_db)):
    try:
        result = EnvironnementService(db).create_environnement(env)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{env_id}", response_model=EnvironnementResponse, status_code=status.HTTP_200_OK, name="Update Environnement")
def update_environnement(env_id: int, env: EnvironnementUpdate, db: Session = Depends(get_db)):
    try:
        result = EnvironnementService(db).update_environnement(env_id, env)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error updating Environnement")

@router.delete("/{env_id}", status_code=status.HTTP_204_NO_CONTENT, name="Delete Environnement")
def delete_environnement(env_id: int, db: Session = Depends(get_db)):
    try:
        EnvironnementService(db).delete_environnement(env_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error deleting Environnement")