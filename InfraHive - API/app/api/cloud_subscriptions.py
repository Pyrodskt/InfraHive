from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud.cloud_subscriptions import CloudSubscriptionService
from app.schemas.cloud_subscriptions import CloudSubscriptionCreate, CloudSubscriptionUpdate, CloudSubscriptionResponse
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[CloudSubscriptionResponse], status_code=status.HTTP_200_OK, name="Get Cloud Subscriptions")
def get_subscriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subscriptions = CloudSubscriptionService(db).get_cloud_subscriptions(skip=skip, limit=limit)
    if not subscriptions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cloud Subscriptions not found")
    return subscriptions

@router.get("/{sub_id}", response_model=CloudSubscriptionResponse, status_code=status.HTTP_200_OK, name="Get Cloud Subscription")
def get_subscription(sub_id: int, db: Session = Depends(get_db)):
    try:
        subscription = CloudSubscriptionService(db).get_cloud_subscription(sub_id)
        return subscription
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=CloudSubscriptionResponse, status_code=status.HTTP_201_CREATED, name="Create Cloud Subscription")
def create_subscription(sub: CloudSubscriptionCreate, db: Session = Depends(get_db)):
    try:
        result = CloudSubscriptionService(db).create_cloud_subscription(sub)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{sub_id}", response_model=CloudSubscriptionResponse, status_code=status.HTTP_200_OK, name="Update Cloud Subscription")
def update_subscription(sub_id: int, sub: CloudSubscriptionUpdate, db: Session = Depends(get_db)):
    try:
        result = CloudSubscriptionService(db).update_cloud_subscription(sub_id, sub)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error updating Cloud Subscription")

@router.delete("/{sub_id}", status_code=status.HTTP_204_NO_CONTENT, name="Delete Cloud Subscription")
def delete_subscription(sub_id: int, db: Session = Depends(get_db)):
    try:
        CloudSubscriptionService(db).delete_cloud_subscription(sub_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error deleting Cloud Subscription")