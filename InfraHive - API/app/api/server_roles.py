
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud.server_roles import ServerRoleService
from app.schemas.server_roles import ServerRoleCreate, ServerRoleUpdate, ServerRoleResponse
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[ServerRoleResponse], status_code=status.HTTP_200_OK, name="Get Server Roles")
def get_server_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    server_roles = ServerRoleService(db).get_server_roles(skip=skip, limit=limit)
    if not server_roles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server Roles not found")
    return server_roles

@router.get("/{role_id}", response_model=ServerRoleResponse, status_code=status.HTTP_200_OK, name="Get Server Role")
def get_server_role(role_id: int, db: Session = Depends(get_db)):
    try:
        server_role = ServerRoleService(db).get_server_role(role_id)
        return server_role
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=ServerRoleResponse, status_code=status.HTTP_201_CREATED, name="Create Server Role")
def create_server_role(role: ServerRoleCreate, db: Session = Depends(get_db)):
    try:
        result = ServerRoleService(db).create_server_role(role)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{role_id}", response_model=ServerRoleResponse, status_code=status.HTTP_200_OK, name="Update Server Role")
def update_server_role(role_id: int, role: ServerRoleUpdate, db: Session = Depends(get_db)):
    try:
        result = ServerRoleService(db).update_server_role(role_id, role)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error updating Server Role")

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT, name="Delete Server Role")
def delete_server_role(role_id: int, db: Session = Depends(get_db)):
    try:
        ServerRoleService(db).delete_server_role(role_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error deleting Server Role")
