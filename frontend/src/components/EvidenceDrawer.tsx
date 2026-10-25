import React, { useState } from 'react';
import { Database, FileText, CloudRain, Globe, ExternalLink, ShieldCheck, Clock } from 'lucide-react';
import { EvidenceData } from '../types';

interface EvidenceDrawerProps {
  evidence: EvidenceData;
}

export const EvidenceDrawer: React.FC<EvidenceDrawerProps> = ({ evidence }) => {
  const [activeTab, setActiveTab] = useState<'sql' | 'docs' | 'weather' | 'web'>('sql');

  const sqlCount = evidence?.sql_queries?.length || 0;
  const docsCount = evidence?.internal_docs?.length || 0;
  const weatherCount = evidence?.weather_records?.length || 0;
  const webCount = evidence?.web_sources?.length || 0;

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg my-5">
      <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-800">
        <h3 className="font-semibold text-sm text-slate-100 flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          Evidence Citations & Verification Logs
        </h3>
        <span className="text-xs text-slate-400">All claims traceable to verified queries & citations</span>
      </div>

      {/* Tab Navigation */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('sql')}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition ${
            activeTab === 'sql'
              ? 'bg-blue-600 text-white'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
          }`}
        >
          <Database className="w-3.5 h-3.5" />
          <span>SQL Queries ({sqlCount})</span>
        </button>
        <button
          onClick={() => setActiveTab('docs')}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition ${
            activeTab === 'docs'
              ? 'bg-emerald-600 text-white'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
          }`}
        >
          <FileText className="w-3.5 h-3.5" />
          <span>Internal SOPs & Reports ({docsCount})</span>
        </button>
        <button
          onClick={() => setActiveTab('weather')}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition ${
            activeTab === 'weather'
              ? 'bg-sky-600 text-white'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
          }`}
        >
          <CloudRain className="w-3.5 h-3.5" />
          <span>Weather Data ({weatherCount})</span>
        </button>
        <button
          onClick={() => setActiveTab('web')}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition ${
            activeTab === 'web'
              ? 'bg-indigo-600 text-white'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
          }`}
        >
          <Globe className="w-3.5 h-3.5" />
          <span>External Market Intel ({webCount})</span>
        </button>
      </div>

      {/* Tab Content Panels */}
      <div className="mt-4">
        {/* Tab 1: SQL Queries */}
        {activeTab === 'sql' && (
          <div className="space-y-3">
            {sqlCount === 0 ? (
              <p className="text-xs text-slate-500 py-4 text-center">No SQL queries executed for this step.</p>
            ) : (
              evidence.sql_queries.map((q, idx) => (
                <div key={idx} className="bg-slate-950 rounded-xl border border-slate-800/80 p-3.5 text-xs space-y-2">
                  <div className="flex items-center justify-between text-slate-400 pb-1.5 border-b border-slate-800">
                    <span className="font-semibold text-slate-200">{q.context}</span>
                    <div className="flex items-center gap-2">
                      <span className="flex items-center gap-1 text-[11px] text-slate-500">
                        <Clock className="w-3 h-3" />
                        {q.duration_ms}ms
                      </span>
                      <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-medium">
                        Read-Only Verified • {q.row_count} rows
                      </span>
                    </div>
                  </div>
                  <pre className="text-slate-300 font-mono text-[11px] bg-slate-900/90 p-2.5 rounded-lg overflow-x-auto selection:bg-blue-600">
                    {q.query.trim()}
                  </pre>
                  <div className="text-[10px] text-slate-500">
                    Tables Accessed: <strong className="text-slate-400">{q.tables.join(', ') || 'reporting views'}</strong>
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {/* Tab 2: Internal Documents */}
        {activeTab === 'docs' && (
          <div className="space-y-3">
            {docsCount === 0 ? (
              <p className="text-xs text-slate-500 py-4 text-center">No internal company documents retrieved.</p>
            ) : (
              evidence.internal_docs.map((doc, idx) => (
                <div key={idx} className="bg-slate-950 rounded-xl border border-slate-800 p-3.5 text-xs space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-emerald-400">{doc.title}</span>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-mono">
                      {doc.citation}
                    </span>
                  </div>
                  <div className="text-[11px] text-slate-400">
                    Department: <strong className="text-slate-300">{doc.department}</strong> • Section: {doc.section}
                  </div>
                  <p className="text-slate-300 bg-slate-900/60 p-2 rounded-lg leading-relaxed text-xs border border-slate-800/60">
                    "{doc.snippet}"
                  </p>
                </div>
              ))
            )}
          </div>
        )}

        {/* Tab 3: Weather Data */}
        {activeTab === 'weather' && (
          <div className="space-y-3">
            {weatherCount === 0 ? (
              <p className="text-xs text-slate-500 py-4 text-center">No weather observations queried.</p>
            ) : (
              evidence.weather_records.map((w, idx) => (
                <div key={idx} className="bg-slate-950 rounded-xl border border-slate-800 p-3.5 text-xs space-y-2">
                  <div className="flex items-center justify-between pb-1 border-b border-slate-800">
                    <span className="font-bold text-sky-400 text-sm">{w.city} Weather Intelligence</span>
                    <span className="text-[11px] text-slate-400">{w.date_range}</span>
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-slate-300">
                    <div className="bg-slate-900 p-2 rounded-lg">
                      <span className="text-slate-500 text-[10px] block">Max Daily Rainfall</span>
                      <strong className="text-base text-sky-400">{w.max_daily_precipitation_mm} mm</strong>
                    </div>
                    <div className="bg-slate-900 p-2 rounded-lg">
                      <span className="text-slate-500 text-[10px] block">Provider</span>
                      <span className="text-xs text-slate-200">{w.source}</span>
                    </div>
                  </div>
                  <div className="p-2 rounded-lg bg-sky-950/30 border border-sky-800/40 text-sky-200 text-xs">
                    <strong>Correlation vs. Causation Analysis:</strong> {w.correlation_assessment}
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {/* Tab 4: External Market Intelligence */}
        {activeTab === 'web' && (
          <div className="space-y-3">
            {webCount === 0 ? (
              <p className="text-xs text-slate-500 py-4 text-center">No external market reports fetched.</p>
            ) : (
              evidence.web_sources.map((web, idx) => (
                <div key={idx} className="bg-slate-950 rounded-xl border border-slate-800 p-3.5 text-xs space-y-1.5">
                  <div className="flex items-center justify-between">
                    <a
                      href={web.url}
                      target="_blank"
                      rel="noreferrer"
                      className="font-semibold text-blue-400 hover:underline flex items-center gap-1"
                    >
                      {web.title}
                      <ExternalLink className="w-3 h-3 text-blue-400" />
                    </a>
                    <span className="text-[10px] text-slate-500">{web.date}</span>
                  </div>
                  <div className="text-[10px] text-slate-400">
                    Source: <strong className="text-slate-300">{web.publisher}</strong>
                  </div>
                  <p className="text-slate-300 bg-slate-900/60 p-2 rounded-lg text-xs border border-slate-800/60">
                    "{web.excerpt}"
                  </p>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
};
