from fastapi import APIRouter, Response
from pydantic import BaseModel
from typing import Optional, Dict, Any
from backend.app.agent.orchestrator import orchestrator
from backend.app.agent.state import WorkspaceState
from backend.app.security.readonly_service import run_readonly_sql
from backend.app.analytics.scratchpad import scratchpad
from backend.app.analytics.pdf_exporter import generate_scratchpad_pdf

router = APIRouter(prefix="/api/workspace", tags=["Workspace"])

class SQLRunRequest(BaseModel):
    query: str
    business_context: Optional[str] = "Manual SQL Console"

@router.get("/initial", response_model=WorkspaceState)
async def get_initial_workspace():
    """Returns a clean, ready starter workspace state without any pre-run queries."""
    from uuid import uuid4
    from backend.app.agent.state import RouteMapData, EvidenceData, FindingsData
    return WorkspaceState(
        investigation_id=str(uuid4()),
        user_query="",
        is_investigating=False,
        current_status="ready",
        timeline=[],
        kpis=[],
        charts=[],
        tables=[],
        route_map=RouteMapData(),
        evidence=EvidenceData(),
        findings=FindingsData(),
        working_memo=[e.model_dump() for e in scratchpad.get_entries()],
        active_scenario=None,
        spoken_response=None,
        conversation_history=[]
    )

@router.post("/sql")
async def execute_raw_readonly_sql(request: SQLRunRequest):
    """Executes read-only SQL with validation checks."""
    return run_readonly_sql(request.query, business_context=request.business_context)

@router.get("/export-pdf")
def export_scratchpad_pdf():
    """Generates and downloads the executive session working memo as a PDF."""
    pdf_bytes = generate_scratchpad_pdf()
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=FreshRoute_Executive_Scenario_Memo.pdf"
        }
    )

@router.get("/scratchpad")
def get_scratchpad_entries():
    """Returns all current working memo entries."""
    return {"entries": [e.model_dump() for e in scratchpad.get_entries()]}
