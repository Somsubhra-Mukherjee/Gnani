from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from backend.app.agent.orchestrator import orchestrator
from backend.app.agent.state import WorkspaceState

router = APIRouter(prefix="/api/chat", tags=["Investigation Chat"])

class InvestigationRequest(BaseModel):
    query: str
    conversation_history: Optional[List[Dict[str, str]]] = []
    existing_workspace: Optional[Dict] = None

@router.post("/investigate", response_model=WorkspaceState)
async def investigate_query(request: InvestigationRequest):
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    workspace = await orchestrator.investigate(
        query=request.query,
        conversation_history=request.conversation_history
    )
    return workspace
