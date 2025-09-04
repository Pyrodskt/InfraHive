from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud.server_sources import ServerSourceService
from app.schemas.server_sources import ServerSourceCreate, ServerSourceUpdate, ServerSourceResponse
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[ServerSourceResponse], status_code=status.HTTP_200_OK, name="Get Server Sources")
def get_sources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sources = ServerSourceService(db).get_server_sources(skip=skip, limit=limit)
    if not sources:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server Sources not found")
    return sources

@router.get("/{source_id}", response_model=ServerSourceResponse, status_code=status.HTTP_200_OK, name="Get Server Source")
def get_source(source_id: int, db: Session = Depends(get_db)):
    try:
        source = ServerSourceService(db).get_server_source(source_id)
        return source
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=ServerSourceResponse, status_code=status.HTTP_201_CREATED, name="Create Server Source")
def create_source(source: ServerSourceCreate, db: Session = Depends(get_db)):
    try:
        result = ServerSourceService(db).create_server_source(source)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{source_id}", response_model=ServerSourceResponse, status_code=status.HTTP_200_OK, name="Update Server Source")
def update_source(source_id: int, source: ServerSourceUpdate, db: Session = Depends(get_db)):
    try:
        result = ServerSourceService(db).update_server_source(source_id, source)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error updating Server Source")

@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT, name="Delete Server Source")
def delete_source(source_id: int, db: Session = Depends(get_db)):
    try:
        ServerSourceService(db).delete_server_source(source_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error deleting Server Source")