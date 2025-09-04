from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud.applications import ApplicationService
from app.schemas.applications import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[ApplicationResponse], status_code=status.HTTP_200_OK, name="Get Applications")
def get_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    applications = ApplicationService(db).get_applications(skip=skip, limit=limit)
    if not applications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Applications not found")
    return applications

@router.get("/{app_id}", response_model=ApplicationResponse, status_code=status.HTTP_200_OK, name="Get Application")
def get_application(app_id: int, db: Session = Depends(get_db)):
    try:
        application = ApplicationService(db).get_application(app_id)
        return application
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED, name="Create Application")
def create_application(app: ApplicationCreate, db: Session = Depends(get_db)):
    try:
        result = ApplicationService(db).create_application(app)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{app_id}", response_model=ApplicationResponse, status_code=status.HTTP_200_OK, name="Update Application")
def update_application(app_id: int, app: ApplicationUpdate, db: Session = Depends(get_db)):
    try:
        result = ApplicationService(db).update_application(app_id, app)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error updating Application")

@router.delete("/{app_id}", status_code=status.HTTP_204_NO_CONTENT, name="Delete Application")
def delete_application(app_id: int, db: Session = Depends(get_db)):
    try:
        ApplicationService(db).delete_application(app_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error deleting Application")

