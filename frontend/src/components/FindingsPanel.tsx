import React from 'react';
import { FindingsData } from '../types';
import { CheckCircle2, Calculator, HelpCircle, AlertOctagon, Lightbulb } from 'lucide-react';

interface FindingsPanelProps {
  findings: FindingsData;
}

export const FindingsPanel: React.FC<FindingsPanelProps> = ({ findings }) => {
  if (!findings || (!findings.observed_facts?.length && !findings.recommended_actions?.length)) {
    return null;
  }

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg my-5 space-y-4">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <h3 className="font-semibold text-sm text-slate-100 flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-blue-400" />
          Structured Findings & Managerial Decisions
        </h3>
        <span className="text-xs text-slate-400">Deterministic Analysis • Gnani Evon v3.3</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* 1. Directly Observed Facts */}
        <div className="bg-slate-950/60 rounded-xl p-4 border border-slate-800/80 space-y-2">
          <h4 className="text-xs font-semibold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5" />
            1. Directly Observed Facts
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

        {/* 2. Plausible Explanations */}
        <div className="bg-slate-950/60 rounded-xl p-4 border border-slate-800/80 space-y-2">
          <h4 className="text-xs font-semibold text-indigo-400 uppercase tracking-wider flex items-center gap-1.5">
            <Calculator className="w-3.5 h-3.5" />
            2. Plausible Root Causes
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

        {/* 3. Unverified Hypotheses & Uncertainty */}
        <div className="bg-slate-950/60 rounded-xl p-4 border border-slate-800/80 space-y-2">
          <h4 className="text-xs font-semibold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
            <AlertOctagon className="w-3.5 h-3.5" />
            3. Uncertainty & Evidence Boundaries
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
              <li className="text-slate-500 italic">No material uncertainty identified.</li>
            )}
          </ul>
        </div>

        {/* 4. Recommended Next Steps */}
        <div className="bg-slate-950/60 rounded-xl p-4 border border-slate-800/80 space-y-2">
          <h4 className="text-xs font-semibold text-blue-400 uppercase tracking-wider flex items-center gap-1.5">
            <Lightbulb className="w-3.5 h-3.5" />
            4. Recommended Action Plan
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
    </div>
  );
};
