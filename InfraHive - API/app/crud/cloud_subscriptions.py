from sqlalchemy.orm import Session
from app.models.all import CloudSubscription
from app.schemas.cloud_subscriptions import CloudSubscriptionCreate, CloudSubscriptionUpdate, CloudSubscriptionResponse
from typing import List

class CloudSubscriptionService:
    def __init__(self, db: Session):
        self.db = db

    def get_cloud_subscription(self, sub_id: int) -> CloudSubscriptionResponse:
        subscription = self.db.query(CloudSubscription).filter(CloudSubscription.id_cloud_subscription == sub_id).first()
        if not subscription:
            raise ValueError("Cloud Subscription not found")
        return CloudSubscriptionResponse.from_orm(subscription)

    def get_cloud_subscriptions(self, skip: int = 0, limit: int = 100) -> List[CloudSubscriptionResponse]:
        subscriptions = self.db.query(CloudSubscription).offset(skip).limit(limit).all()
        return [CloudSubscriptionResponse.from_orm(sub) for sub in subscriptions]

    def create_cloud_subscription(self, sub: CloudSubscriptionCreate) -> CloudSubscriptionResponse:
        new_subscription = CloudSubscription(**sub.model_dump())
        self.db.add(new_subscription)
        self.db.commit()
        self.db.refresh(new_subscription)
        return CloudSubscriptionResponse.from_orm(new_subscription)

    def update_cloud_subscription(self, sub_id: int, sub: CloudSubscriptionUpdate) -> CloudSubscriptionResponse:
        existing_subscription = self.db.query(CloudSubscription).filter(CloudSubscription.id_cloud_subscription == sub_id).first()
        if not existing_subscription:
            raise ValueError("Cloud Subscription not found")
        for key, value in sub.model_dump(exclude_unset=True).items():
            setattr(existing_subscription, key, value)
        self.db.commit()
        self.db.refresh(existing_subscription)
        return CloudSubscriptionResponse.from_orm(existing_subscription)

    def delete_cloud_subscription(self, sub_id: int):
        existing_subscription = self.db.query(CloudSubscription).filter(CloudSubscription.id_cloud_subscription == sub_id).first()
        if not existing_subscription:
            raise ValueError("Cloud Subscription not found")
        self.db.delete(existing_subscription)
        self.db.commit()
        return None