from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class KPICard(BaseModel):
    label: str
    value: str
    delta: Optional[str] = None
    trend: Optional[str] = "neutral"  # "positive", "negative", "neutral"
    unit: Optional[str] = None
    subtitle: Optional[str] = None
    color: Optional[str] = "blue"

class ChartSeries(BaseModel):
    name: str
    data_key: str
    color: str

class ChartConfig(BaseModel):
    chart_id: str
    title: str
    chart_type: str  # "line", "bar", "pie", "area"
    data: List[Dict[str, Any]]
    x_axis_key: str
    series: List[ChartSeries]

class DataTable(BaseModel):
    table_id: str
    title: str
    columns: List[str]
    rows: List[Dict[str, Any]]

class RouteMarker(BaseModel):
    name: str
    latitude: float
    longitude: float
    marker_type: str  # "hub", "depot", "incident"
    description: Optional[str] = None

class RouteMapData(BaseModel):
    routes: List[Dict[str, Any]] = []
    markers: List[RouteMarker] = []

class EvidenceData(BaseModel):
    sql_queries: List[Dict[str, Any]] = []
    internal_docs: List[Dict[str, Any]] = []
    weather_records: List[Dict[str, Any]] = []
    web_sources: List[Dict[str, Any]] = []

class FindingsData(BaseModel):
    observed_facts: List[str] = []
    calculated_metrics: Dict[str, Any] = {}
    plausible_explanations: List[str] = []
    unverified_hypotheses: List[str] = []
    recommended_actions: List[str] = []

class SpokenResponse(BaseModel):
    text: str
    audio_base64: Optional[str] = None
    audio_format: str = "wav"
    voice: str = "Gnani-Timbre-Indian-English"
    client_speech_fallback: bool = True

class InvestigationStep(BaseModel):
    step_id: int
    action: str  # "planning", "querying_sql", "retrieving_docs", "weather_lookup", "calculating", "updating_canvas", "speaking"
    status: str  # "in_progress", "completed", "rejected"
    detail: str
    timestamp: str

class WorkspaceState(BaseModel):
    investigation_id: str
    user_query: str
    is_investigating: bool = False
    current_status: str = "idle"
    timeline: List[InvestigationStep] = []
    kpis: List[KPICard] = []
    charts: List[ChartConfig] = []
    tables: List[DataTable] = []
    route_map: RouteMapData = RouteMapData()
    evidence: EvidenceData = EvidenceData()
    findings: FindingsData = FindingsData()
    spoken_response: Optional[SpokenResponse] = None
    conversation_history: List[Dict[str, str]] = []
