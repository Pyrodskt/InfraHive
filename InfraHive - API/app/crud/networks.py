from sqlalchemy.orm import Session
from app.models.all import Network
from app.schemas.networks import NetworkCreate, NetworkUpdate, NetworkResponse
from typing import List

class NetworkService:
    def __init__(self, db: Session):
        self.db = db

    def get_network(self, network_id: int) -> NetworkResponse:
        network = self.db.query(Network).filter(Network.id_network == network_id).first()
        if not network:
            raise ValueError("Network not found")
        return NetworkResponse.from_orm(network)

    def get_networks(self, skip: int = 0, limit: int = 100) -> List[NetworkResponse]:
        networks = self.db.query(Network).offset(skip).limit(limit).all()
        return [NetworkResponse.from_orm(network) for network in networks]

    def create_network(self, network: NetworkCreate) -> NetworkResponse:
        new_network = Network(**network.model_dump())
        self.db.add(new_network)
        self.db.commit()
        self.db.refresh(new_network)
        return NetworkResponse.from_orm(new_network)

    def update_network(self, network_id: int, network: NetworkUpdate) -> NetworkResponse:
        existing_network = self.db.query(Network).filter(Network.id_network == network_id).first()
        if not existing_network:
            raise ValueError("Network not found")
        for key, value in network.model_dump(exclude_unset=True).items():
            setattr(existing_network, key, value)
        self.db.commit()
        self.db.refresh(existing_network)
        return NetworkResponse.from_orm(existing_network)

    def delete_network(self, network_id: int):
        existing_network = self.db.query(Network).filter(Network.id_network == network_id).first()
        if not existing_network:
            raise ValueError("Network not found")
        self.db.delete(existing_network)
        self.db.commit()
        return None