import React from 'react';
import { WorkspaceState, VoiceState } from '../types';
import { VoiceController } from './VoiceController';
import { InvestigationTimeline } from './InvestigationTimeline';
import { SpokenPlayer } from './SpokenPlayer';
import { KpiCards } from './KpiCards';
import { MetricCharts } from './MetricCharts';
import { RouteMap } from './RouteMap';
import { DataTableSection } from './DataTableSection';
import { FindingsPanel } from './FindingsPanel';
import { EvidenceDrawer } from './EvidenceDrawer';
import { LayoutDashboard } from 'lucide-react';

interface WorkspaceCanvasProps {
  workspace: WorkspaceState;
  voiceState: VoiceState;
  onTranscriptReady: (transcript: string) => void;
  onVoiceStateChange: (state: VoiceState) => void;
}

export const WorkspaceCanvas: React.FC<WorkspaceCanvasProps> = ({
  workspace,
  voiceState,
  onTranscriptReady,
  onVoiceStateChange
}) => {
  return (
    <div className="space-y-6">
      {/* Voice Interaction Hero Area */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-3xl p-6 text-center backdrop-blur shadow-xl relative overflow-hidden">
        <div className="absolute -top-24 -left-24 w-72 h-72 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute -bottom-24 -right-24 w-72 h-72 bg-purple-600/10 rounded-full blur-3xl pointer-events-none"></div>

        <VoiceController
          currentState={voiceState}
          onTranscriptReady={onTranscriptReady}
          onStateChange={onVoiceStateChange}
        />

        {workspace.user_query && (
          <div className="mt-2 inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-950/80 border border-slate-800 text-xs text-slate-300">
            <span className="text-slate-500">Current Investigation:</span>
            <strong className="text-slate-100">"{workspace.user_query}"</strong>
          </div>
        )}
      </div>

      {/* Investigation Progress Timeline */}
      <InvestigationTimeline
        timeline={workspace.timeline}
        isInvestigating={workspace.is_investigating}
      />

      {/* Spoken Verbal Findings Player */}
      {workspace.spoken_response && (
        <SpokenPlayer spokenResponse={workspace.spoken_response} />
      )}

      {/* Core Analytical Canvas */}
      <div className="space-y-6">
        {/* KPI Cards */}
        <KpiCards kpis={workspace.kpis} />

        {/* Interactive Charts */}
        <MetricCharts charts={workspace.charts} />

        {/* Route Surveillance Map */}
        <RouteMap routeMap={workspace.route_map} />

        {/* Detailed Data Tables */}
        <DataTableSection tables={workspace.tables} />

        {/* Structured Findings & Managerial Decisions */}
        <FindingsPanel findings={workspace.findings} />

        {/* Evidence & Verification Logs */}
        <EvidenceDrawer evidence={workspace.evidence} />
      </div>
    </div>
  );
};
