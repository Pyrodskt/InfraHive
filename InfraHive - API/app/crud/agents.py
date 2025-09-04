from sqlalchemy.orm import Session
from app.models.all import Agents
from app.schemas.agents import AgentsCreate, AgentsUpdate, AgentsResponse
from typing import List

class AgentsService:
    def __init__(self, db: Session):
        self.db = db

    def get_agent(self, agent_id: int) -> AgentsResponse:
        agent = self.db.query(Agents).filter(Agents.id_agent == agent_id).first()
        if not agent:
            raise ValueError("Agent not found")
        return AgentsResponse.from_orm(agent)

    def get_agents(self, skip: int = 0, limit: int = 100) -> List[AgentsResponse]:
        agents = self.db.query(Agents).offset(skip).limit(limit).all()
        return [AgentsResponse.from_orm(agent) for agent in agents]

    def create_agent(self, agent: AgentsCreate) -> AgentsResponse:
        new_agent = Agents(**agent.model_dump())
        self.db.add(new_agent)
        self.db.commit()
        self.db.refresh(new_agent)
        return AgentsResponse.from_orm(new_agent)

    def update_agent(self, agent_id: int, agent: AgentsUpdate) -> AgentsResponse:
        existing_agent = self.db.query(Agents).filter(Agents.id_agent == agent_id).first()
        if not existing_agent:
            raise ValueError("Agent not found")
        for key, value in agent.model_dump(exclude_unset=True).items():
            setattr(existing_agent, key, value)
        self.db.commit()
        self.db.refresh(existing_agent)
        return AgentsResponse.from_orm(existing_agent)

    def delete_agent(self, agent_id: int):
        existing_agent = self.db.query(Agents).filter(Agents.id_agent == agent_id).first()
        if not existing_agent:
            raise ValueError("Agent not found")
        self.db.delete(existing_agent)
        self.db.commit()
        return None