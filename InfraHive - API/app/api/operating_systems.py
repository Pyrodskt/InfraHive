from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud.operating_systems import OperatingSystemService
from app.schemas import operating_systems as schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.OperatingSystemResponse], status_code=status.HTTP_200_OK, name="Get Operating systems")
def get_oss(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    oss = OperatingSystemService(db).get_operating_systems(skip=skip, limit=limit)
    if not oss:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operating systems not found")
    return oss

@router.get("/{os_id}", response_model=schemas.OperatingSystemResponse, status_code=status.HTTP_200_OK, name="Get Operating system")
def get_os(os_id: int, db: Session = Depends(get_db)):
    db_os = OperatingSystemService(db).get_operating_system(os_id=os_id)
    if db_os is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operating System not found")
    return db_os

@router.post("/", response_model=schemas.OperatingSystemResponse, status_code=status.HTTP_201_CREATED, name="Create Operating system")
def create_os(os: schemas.OperatingSystemCreate, db: Session = Depends(get_db)):
    result = OperatingSystemService(db).create_operating_system(os)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creation Operating System")
    return result

@router.put("/{os_id}", response_model=schemas.OperatingSystemResponse, status_code=status.HTTP_200_OK, name="Update Operating system")
def update_os(os_id:int, os:schemas.OperatingSystemUpdate, db: Session = Depends(get_db)):
    try:
        result = OperatingSystemService(db).update_operating_system(os_id, os)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error updating Operating System")

@router.delete("/{os_id}", status_code=status.HTTP_204_NO_CONTENT, name="Delete Operating sytem")
def delete_os(os_id:int, db:Session=Depends(get_db)):
    try:
        OperatingSystemService(db).delete_operating_system(os_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error deleting Operating System")