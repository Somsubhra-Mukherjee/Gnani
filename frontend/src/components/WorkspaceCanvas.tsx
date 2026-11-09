import React, { useState } from 'react';
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
import { LayoutDashboard, Sparkles, Send } from 'lucide-react';

interface WorkspaceCanvasProps {
  workspace: WorkspaceState;
  voiceState: VoiceState;
  onTranscriptReady: (transcript: string) => void;
  onVoiceStateChange: (state: VoiceState) => void;
  onSendMessage?: (msg: string) => void;
}

const QUICK_INQUIRIES = [
  "What is the cost of per piece production in Gujarat?",
  "What is the cost of per piece transportation in Gujarat?",
  "Add both numbers and give total landed cost in Gujarat",
  "What are the numbers for West Bengal?",
  "Shift 2% volume from Gujarat to West Bengal",
  "What are the top 3 warehouses by storage capacity?"
];

export const WorkspaceCanvas: React.FC<WorkspaceCanvasProps> = ({
  workspace,
  voiceState,
  onTranscriptReady,
  onVoiceStateChange,
  onSendMessage
}) => {
  const [inputText, setInputText] = useState('');

  const handleTextSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim() || voiceState === 'investigating') return;
    if (onSendMessage) {
      onSendMessage(inputText.trim());
    } else {
      onTranscriptReady(inputText.trim());
    }
    setInputText('');
  };

  return (
    <div className="space-y-6">
      {/* Voice & Query Interaction Hero Area (Clean, no background blur blobs or pulsing shadows) */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 text-center relative">

        <VoiceController
          currentState={voiceState}
          onTranscriptReady={onTranscriptReady}
          onStateChange={onVoiceStateChange}
        />

        {/* Text Input Bar */}
        <form
          onSubmit={handleTextSubmit}
          className="mt-4 max-w-xl mx-auto flex items-center gap-2 bg-slate-950/80 border border-slate-800 rounded-full p-1.5 focus-within:border-blue-500 transition shadow-inner"
        >
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Ask your business a question (or use mic above)..."
            className="flex-1 bg-transparent px-4 py-1.5 text-xs text-slate-100 placeholder-slate-500 outline-none"
          />
          <button
            type="submit"
            disabled={!inputText.trim() || voiceState === 'investigating'}
            className="px-4 py-1.5 bg-blue-600 hover:bg-blue-500 disabled:opacity-40 text-white text-xs font-medium rounded-full transition flex items-center gap-1.5"
          >
            <span>Ask</span>
            <Send className="w-3 h-3" />
          </button>
        </form>

        {/* Quick Suggestion Pills */}
        <div className="mt-3 flex flex-wrap justify-center gap-1.5 max-w-3xl mx-auto">
          {QUICK_INQUIRIES.map((pill, i) => (
            <button
              key={i}
              type="button"
              onClick={() => onSendMessage && onSendMessage(pill)}
              className="text-[11px] px-3 py-1 rounded-full bg-slate-800/60 hover:bg-slate-700/80 text-slate-300 border border-slate-700/50 transition hover:border-slate-500 cursor-pointer"
            >
              {pill}
            </button>
          ))}
        </div>

        {workspace.user_query && (
          <div className="mt-4 inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-950/80 border border-slate-800 text-xs text-slate-300">
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
        <FindingsPanel findings={workspace.findings} workingMemo={workspace.working_memo} />

        {/* Evidence & Verification Logs */}
        <EvidenceDrawer evidence={workspace.evidence} />
      </div>
    </div>
  );
};
