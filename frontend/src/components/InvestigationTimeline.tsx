import React from 'react';
import { Database, FileText, CloudRain, Calculator, Volume2, ShieldAlert, CheckCircle2, Loader2, Sparkles } from 'lucide-react';
import { InvestigationStep } from '../types';

interface TimelineProps {
  timeline: InvestigationStep[];
  isInvestigating: boolean;
}

export const InvestigationTimeline: React.FC<TimelineProps> = ({ timeline, isInvestigating }) => {
  if (timeline.length === 0 && !isInvestigating) return null;

  const getStepIcon = (action: string, status: string) => {
    if (status === 'rejected') return <ShieldAlert className="w-4 h-4 text-red-400" />;
    if (status === 'in_progress') return <Loader2 className="w-4 h-4 animate-spin text-blue-400" />;

    switch (action) {
      case 'intent_understanding':
      case 'planning':
        return <Sparkles className="w-4 h-4 text-indigo-400" />;
      case 'querying_sql':
        return <Database className="w-4 h-4 text-blue-400" />;
      case 'retrieving_docs':
        return <FileText className="w-4 h-4 text-emerald-400" />;
      case 'weather_lookup':
        return <CloudRain className="w-4 h-4 text-sky-400" />;
      case 'calculating':
        return <Calculator className="w-4 h-4 text-amber-400" />;
      case 'speaking':
        return <Volume2 className="w-4 h-4 text-purple-400" />;
      default:
        return <CheckCircle2 className="w-4 h-4 text-slate-400" />;
    }
  };

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 my-4">
      <div className="flex items-center justify-between mb-3 pb-2 border-b border-slate-800">
        <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-2">
          <Sparkles className="w-3.5 h-3.5 text-blue-400" />
          Autonomous Investigation Timeline
        </h3>
        {isInvestigating && (
          <span className="flex items-center gap-1.5 text-xs text-blue-400">
            <Loader2 className="w-3 h-3 animate-spin" />
            Analyzing evidence...
          </span>
        )}
      </div>

      <div className="space-y-2.5">
        {timeline.map((step) => (
          <div
            key={step.step_id}
            className={`flex items-start gap-3 p-2 rounded-lg text-xs transition ${
              step.status === 'rejected'
                ? 'bg-red-500/10 border border-red-500/20 text-red-200'
                : 'bg-slate-950/40 border border-slate-800/80 text-slate-300'
            }`}
          >
            <div className="mt-0.5">{getStepIcon(step.action, step.status)}</div>
            <div className="flex-1">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-slate-200 capitalize">
                  {step.action.replace('_', ' ')}
                </span>
                <span className="text-[10px] text-slate-500">{step.timestamp}</span>
              </div>
              <p className="text-slate-400 text-xs mt-0.5">{step.detail}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
