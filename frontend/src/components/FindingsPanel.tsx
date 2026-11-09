import React from 'react';
import { FindingsData } from '../types';
import { CheckCircle2, Calculator, AlertOctagon, FileDown, Scale } from 'lucide-react';

interface FindingsPanelProps {
  findings: FindingsData;
  workingMemo?: {
    id: number;
    timestamp: string;
    query: string;
    category: string;
    details: string;
    formula?: string;
  }[];
}

export const FindingsPanel: React.FC<FindingsPanelProps> = ({ findings, workingMemo }) => {
  if (!findings || (!findings.observed_facts?.length && !findings.recommended_actions?.length)) {
    return null;
  }

  const handleExportPdf = () => {
    window.open('/api/workspace/export-pdf', '_blank');
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg my-5 space-y-4">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <Scale className="w-5 h-5 text-blue-400" />
          <div>
            <h3 className="font-semibold text-sm text-slate-100">
              Executive Scratchpad & Decision Balance Sheet
            </h3>
            <p className="text-[11px] text-slate-400">
              Objective Quant Assistant • Strategic Judgment Rests with Leadership
            </p>
          </div>
        </div>
        <button
          onClick={handleExportPdf}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/40 text-blue-300 text-xs font-medium transition"
        >
          <FileDown className="w-3.5 h-3.5" />
          <span>Export Memo (PDF)</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* 1. Directly Observed Facts */}
        <div className="bg-slate-950/60 rounded-xl p-4 border border-slate-800/80 space-y-2">
          <h4 className="text-xs font-semibold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5" />
            1. Verified Facts & Database Extractions
          </h4>
          <ul className="space-y-1.5 text-xs text-slate-300">
            {findings.observed_facts?.map((fact, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-emerald-400 font-bold">•</span>
                <span>{fact}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* 2. Mathematical Arithmetic Applied */}
        <div className="bg-slate-950/60 rounded-xl p-4 border border-slate-800/80 space-y-2">
          <h4 className="text-xs font-semibold text-indigo-400 uppercase tracking-wider flex items-center gap-1.5">
            <Calculator className="w-3.5 h-3.5" />
            2. Deterministic Formulas & Computations
          </h4>
          <ul className="space-y-1.5 text-xs text-slate-300">
            {findings.plausible_explanations?.map((exp, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-indigo-400 font-bold">•</span>
                <span>{exp}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* 3. Evidence Boundaries & Assumptions */}
        <div className="bg-slate-950/60 rounded-xl p-4 border border-slate-800/80 space-y-2">
          <h4 className="text-xs font-semibold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
            <AlertOctagon className="w-3.5 h-3.5" />
            3. Model Assumptions & Operational Scope
          </h4>
          <ul className="space-y-1.5 text-xs text-slate-300">
            {findings.unverified_hypotheses?.length ? (
              findings.unverified_hypotheses.map((hyp, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-amber-400 font-bold">•</span>
                  <span>{hyp}</span>
                </li>
              ))
            ) : (
              <li className="text-slate-500 italic">No external operational constraints assumed in this step.</li>
            )}
          </ul>
        </div>

        {/* 4. Strategic Decision Space (Neutral) */}
        <div className="bg-slate-950/60 rounded-xl p-4 border border-slate-800/80 space-y-2">
          <h4 className="text-xs font-semibold text-blue-400 uppercase tracking-wider flex items-center gap-1.5">
            <Scale className="w-3.5 h-3.5" />
            4. Executive Strategic Space
          </h4>
          <ul className="space-y-1.5 text-xs text-slate-300">
            {findings.recommended_actions?.map((act, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-blue-400 font-bold">•</span>
                <span>{act}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Active Session Scratchpad Log */}
      {workingMemo && workingMemo.length > 0 && (
        <div className="mt-4 pt-3 border-t border-slate-800/80">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
              Active Session Scratchpad Log ({workingMemo.length} steps recorded)
            </span>
          </div>
          <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
            {workingMemo.map((entry) => (
              <div
                key={entry.id}
                className="p-2.5 rounded-lg bg-slate-950/80 border border-slate-800 text-xs flex flex-col gap-1"
              >
                <div className="flex items-center justify-between text-slate-400 text-[10px]">
                  <span className="font-semibold text-blue-400">Step {entry.id}: {entry.category}</span>
                  <span>{entry.timestamp}</span>
                </div>
                <div className="text-slate-200 font-medium">"{entry.query}"</div>
                <div className="text-slate-400 text-[11px]">{entry.details}</div>
                {entry.formula && (
                  <div className="text-[11px] font-mono text-emerald-400 bg-emerald-950/30 px-2 py-0.5 rounded border border-emerald-900/40 inline-block w-fit">
                    {entry.formula}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
