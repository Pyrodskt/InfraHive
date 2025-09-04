from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud.server_tiers import ServerTierService
from app.schemas.server_tiers import ServerTierCreate, ServerTierUpdate, ServerTierResponse
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[ServerTierResponse], status_code=status.HTTP_200_OK, name="Get Server Tiers")
def get_server_tiers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    server_tiers = ServerTierService(db).get_server_tiers(skip=skip, limit=limit)
    if not server_tiers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server Tiers not found")
    return server_tiers

@router.get("/{tier_id}", response_model=ServerTierResponse, status_code=status.HTTP_200_OK, name="Get Server Tier")
def get_server_tier(tier_id: int, db: Session = Depends(get_db)):
    try:
        server_tier = ServerTierService(db).get_server_tier(tier_id)
        return server_tier
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=ServerTierResponse, status_code=status.HTTP_201_CREATED, name="Create Server Tier")
def create_server_tier(tier: ServerTierCreate, db: Session = Depends(get_db)):
    try:
        result = ServerTierService(db).create_server_tier(tier)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{tier_id}", response_model=ServerTierResponse, status_code=status.HTTP_200_OK, name="Update Server Tier")
def update_server_tier(tier_id: int, tier: ServerTierUpdate, db: Session = Depends(get_db)):
    try:
        result = ServerTierService(db).update_server_tier(tier_id, tier)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error updating Server Tier")

@router.delete("/{tier_id}", status_code=status.HTTP_204_NO_CONTENT, name="Delete Server Tier")
def delete_server_tier(tier_id: int, db: Session = Depends(get_db)):
    try:
        ServerTierService(db).delete_server_tier(tier_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error deleting Server Tier")
