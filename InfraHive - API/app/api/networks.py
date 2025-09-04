from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud.networks import NetworkService
from app.schemas.networks import NetworkCreate, NetworkUpdate, NetworkResponse
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[NetworkResponse], status_code=status.HTTP_200_OK, name="Get Networks")
def get_networks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    networks = NetworkService(db).get_networks(skip=skip, limit=limit)
    if not networks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Networks not found")
    return networks

@router.get("/{network_id}", response_model=NetworkResponse, status_code=status.HTTP_200_OK, name="Get Network")
def get_network(network_id: int, db: Session = Depends(get_db)):
    try:
        network = NetworkService(db).get_network(network_id)
        return network
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=NetworkResponse, status_code=status.HTTP_201_CREATED, name="Create Network")
def create_network(network: NetworkCreate, db: Session = Depends(get_db)):
    try:
        result = NetworkService(db).create_network(network)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{network_id}", response_model=NetworkResponse, status_code=status.HTTP_200_OK, name="Update Network")
def update_network(network_id: int, network: NetworkUpdate, db: Session = Depends(get_db)):
    try:
        result = NetworkService(db).update_network(network_id, network)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error updating Network")

@router.delete("/{network_id}", status_code=status.HTTP_204_NO_CONTENT, name="Delete Network")
def delete_network(network_id: int, db: Session = Depends(get_db)):
    try:
        NetworkService(db).delete_network(network_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error deleting Network")