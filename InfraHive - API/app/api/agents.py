from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud.agents import AgentsService
from app.schemas.agents import AgentsCreate, AgentsUpdate, AgentsResponse
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[AgentsResponse], status_code=status.HTTP_200_OK, name="Get Agents")
def get_agents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    agents = AgentsService(db).get_agents(skip=skip, limit=limit)
    if not agents:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agents not found")
    return agents

@router.get("/{agent_id}", response_model=AgentsResponse, status_code=status.HTTP_200_OK, name="Get Agent")
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    try:
        agent = AgentsService(db).get_agent(agent_id)
        return agent
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=AgentsResponse, status_code=status.HTTP_201_CREATED, name="Create Agent")
def create_agent(agent: AgentsCreate, db: Session = Depends(get_db)):
    try:
        result = AgentsService(db).create_agent(agent)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{agent_id}", response_model=AgentsResponse, status_code=status.HTTP_200_OK, name="Update Agent")
def update_agent(agent_id: int, agent: AgentsUpdate, db: Session = Depends(get_db)):
    try:
        result = AgentsService(db).update_agent(agent_id, agent)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error updating Agent")

@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT, name="Delete Agent")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    try:
        AgentsService(db).delete_agent(agent_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error deleting Agent")