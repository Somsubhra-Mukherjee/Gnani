import React from 'react';
import { ShieldCheck, Cpu, Mic, Volume2 } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-40 px-6 py-3 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/20">
          FR
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="font-bold text-lg text-slate-100 tracking-tight">FreshRoute Foods</h1>
            <span className="px-2 py-0.5 text-xs font-medium rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
              Voice BI Agent
            </span>
          </div>
          <p className="text-xs text-slate-400">Great Indian AI Internship Challenge 2026 • Gnani.ai</p>
        </div>
      </div>

      <div className="hidden lg:flex items-center gap-4 text-xs">
        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/60 border border-slate-700/60 text-slate-300">
          <Mic className="w-3.5 h-3.5 text-blue-400" />
          <span>STT: <strong className="text-slate-100">Prisma v2.5</strong></span>
        </div>
        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/60 border border-slate-700/60 text-slate-300">
          <Cpu className="w-3.5 h-3.5 text-indigo-400" />
          <span>LLM: <strong className="text-slate-100">Evon v3.3</strong></span>
        </div>
        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/60 border border-slate-700/60 text-slate-300">
          <Volume2 className="w-3.5 h-3.5 text-purple-400" />
          <span>TTS: <strong className="text-slate-100">Timbre v2.5</strong></span>
        </div>
        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-medium">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span>SQL: Read-Only Enforced</span>
        </div>
      </div>
    </header>
  );
};
