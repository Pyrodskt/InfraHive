from sqlalchemy.orm import Session
from app.models.all import Application
from app.schemas.applications import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from typing import List

class ApplicationService:
    def __init__(self, db: Session):
        self.db = db

    def get_application(self, app_id: int) -> ApplicationResponse:
        application = self.db.query(Application).filter(Application.id_application == app_id).first()
        if not application:
            raise ValueError("Application not found")
        return ApplicationResponse.from_orm(application)

    def get_applications(self, skip: int = 0, limit: int = 100) -> List[ApplicationResponse]:
        applications = self.db.query(Application).offset(skip).limit(limit).all()
        return [ApplicationResponse.from_orm(app) for app in applications]

    def create_application(self, app: ApplicationCreate) -> ApplicationResponse:
        new_app = Application(**app.model_dump())
        self.db.add(new_app)
        self.db.commit()
        self.db.refresh(new_app)
        return ApplicationResponse.from_orm(new_app)

    def update_application(self, app_id: int, app: ApplicationUpdate) -> ApplicationResponse:
        existing_app = self.db.query(Application).filter(Application.id_application == app_id).first()
        if not existing_app:
            raise ValueError("Application not found")
        for key, value in app.model_dump(exclude_unset=True).items():
            setattr(existing_app, key, value)
        self.db.commit()
        self.db.refresh(existing_app)
        return ApplicationResponse.from_orm(existing_app)

    def delete_application(self, app_id: int):
        existing_app = self.db.query(Application).filter(Application.id_application == app_id).first()
        if not existing_app:
            raise ValueError("Application not found")
        self.db.delete(existing_app)
        self.db.commit()
        return None