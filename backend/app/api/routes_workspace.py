from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any
from backend.app.agent.orchestrator import orchestrator
from backend.app.agent.state import WorkspaceState
from backend.app.security.readonly_service import run_readonly_sql

router = APIRouter(prefix="/api/workspace", tags=["Workspace"])

class SQLRunRequest(BaseModel):
    query: str
    business_context: Optional[str] = "Manual SQL Console"

@router.get("/initial", response_model=WorkspaceState)
async def get_initial_workspace():
    """Returns baseline starter workspace state."""
    init_state = await orchestrator.investigate("Why did our profits decline in North India in August 2024?")
    return init_state

@router.post("/sql")
async def execute_raw_readonly_sql(request: SQLRunRequest):
    """Executes read-only SQL with validation checks."""
    return run_readonly_sql(request.query, business_context=request.business_context)
