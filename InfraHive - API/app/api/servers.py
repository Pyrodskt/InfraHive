from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud.servers import ServerService
from app.schemas.servers import ServerCreate, ServerUpdate, ServerResponse
from app.schemas.detailled import ServerResponseDetailled
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[ServerResponse], status_code=status.HTTP_200_OK, name="Get Servers")
def get_servers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    servers = ServerService(db).get_servers(skip=skip, limit=limit)
    if not servers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servers not found")
    return servers

@router.get("/{server_id}", response_model=ServerResponse, status_code=status.HTTP_200_OK, name="Get Server")
def get_server(server_id: int, db: Session = Depends(get_db)):
    try:
        server = ServerService(db).get_server(server_id)
        return server
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/{server_id}/detailled", response_model=ServerResponseDetailled, status_code=status.HTTP_200_OK, name="Get server detailled")
def get_server_detailled(server_id: int, db: Session = Depends(get_db)):
    try:
        server = ServerService(db).get_server_detailled(server_id)
        return server
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=ServerResponse, status_code=status.HTTP_201_CREATED, name="Create Server")
def create_server(server: ServerCreate, db: Session = Depends(get_db)):
    try:
        result = ServerService(db).create_server(server)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{server_id}", response_model=ServerResponse, status_code=status.HTTP_200_OK, name="Update Server")
def update_server(server_id: int, server: ServerUpdate, db: Session = Depends(get_db)):
    try:
        result = ServerService(db).update_server(server_id, server)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error updating Server")

@router.delete("/{server_id}", status_code=status.HTTP_204_NO_CONTENT, name="Delete Server")
def delete_server(server_id: int, db: Session = Depends(get_db)):
    try:
        ServerService(db).delete_server(server_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error deleting Server")