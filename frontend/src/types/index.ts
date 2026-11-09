export interface KPICard {
  label: string;
  value: string;
  delta?: string;
  trend?: 'positive' | 'negative' | 'neutral';
  unit?: string;
  subtitle?: string;
  color?: string;
}

export interface ChartSeries {
  name: string;
  data_key: string;
  color: string;
}

export interface ChartConfig {
  chart_id: string;
  title: string;
  chart_type: 'line' | 'bar' | 'pie' | 'area';
  data: Record<string, any>[];
  x_axis_key: string;
  series: ChartSeries[];
}

export interface DataTable {
  table_id: string;
  title: string;
  columns: string[];
  rows: Record<string, any>[];
}

export interface RouteMarker {
  name: string;
  latitude: number;
  longitude: number;
  marker_type: string;
  description?: string;
}

export interface RouteItem {
  code: string;
  origin: string;
  dest: string;
  distance_km: number;
  avg_cost_km: number;
  status: string;
}

export interface RouteMapData {
  routes: RouteItem[];
  markers: RouteMarker[];
}

export interface EvidenceData {
  sql_queries: {
    context: string;
    query: string;
    row_count: number;
    duration_ms: number;
    tables: string[];
  }[];
  internal_docs: {
    doc_id: string;
    title: string;
    section: string;
    citation: string;
    department: string;
    snippet: string;
  }[];
  weather_records: {
    city: string;
    date_range: string;
    source: string;
    max_daily_precipitation_mm: number;
    correlation_assessment: string;
  }[];
  web_sources: {
    title: string;
    publisher: string;
    url: string;
    date: string;
    excerpt: string;
  }[];
}

export interface FindingsData {
  observed_facts: string[];
  calculated_metrics: Record<string, any>;
  plausible_explanations: string[];
  unverified_hypotheses: string[];
  recommended_actions: string[];
}

export interface SpokenResponse {
  text: string;
  audio_base64?: string;
  audio_format: string;
  voice: string;
  client_speech_fallback: boolean;
}

export interface InvestigationStep {
  step_id: number;
  action: string;
  status: 'in_progress' | 'completed' | 'rejected';
  detail: string;
  timestamp: string;
}

export interface WorkspaceState {
  investigation_id: string;
  user_query: string;
  is_investigating: boolean;
  current_status: string;
  timeline: InvestigationStep[];
  kpis: KPICard[];
  charts: ChartConfig[];
  tables: DataTable[];
  route_map: RouteMapData;
  evidence: EvidenceData;
  findings: FindingsData;
  working_memo?: {
    id: number;
    timestamp: string;
    query: string;
    category: string;
    details: string;
    formula?: string;
  }[];
  active_scenario?: Record<string, any>;
  spoken_response?: SpokenResponse;
  conversation_history: { role: string; content: string }[];
}

export type VoiceState = 'idle' | 'listening' | 'transcribing' | 'confirming' | 'investigating' | 'speaking';
