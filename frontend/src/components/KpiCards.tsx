import React from 'react';
import { ArrowUpRight, ArrowDownRight, Minus, TrendingUp } from 'lucide-react';
import { KPICard } from '../types';

interface KpiCardsProps {
  kpis: KPICard[];
}

export const KpiCards: React.FC<KpiCardsProps> = ({ kpis }) => {
  if (!kpis || kpis.length === 0) return null;

  const getColorClasses = (color?: string, trend?: string) => {
    if (color === 'red' || trend === 'negative') {
      return {
        border: 'border-rose-500/20 hover:border-rose-500/40',
        badge: 'bg-rose-500/10 text-rose-400 border border-rose-500/20',
        text: 'text-rose-400'
      };
    }
    if (color === 'green' || trend === 'positive') {
      return {
        border: 'border-emerald-500/20 hover:border-emerald-500/40',
        badge: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
        text: 'text-emerald-400'
      };
    }
    if (color === 'orange') {
      return {
        border: 'border-amber-500/20 hover:border-amber-500/40',
        badge: 'bg-amber-500/10 text-amber-400 border border-amber-500/20',
        text: 'text-amber-400'
      };
    }
    return {
      border: 'border-blue-500/20 hover:border-blue-500/40',
      badge: 'bg-blue-500/10 text-blue-400 border border-blue-500/20',
      text: 'text-blue-400'
    };
  };

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 my-4">
      {kpis.map((kpi, idx) => {
        const style = getColorClasses(kpi.color, kpi.trend);
        return (
          <div
            key={idx}
            className={`bg-slate-900/80 rounded-2xl p-5 border ${style.border} transition-all duration-200 hover:shadow-lg hover:-translate-y-0.5`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-medium text-slate-400 tracking-wide">{kpi.label}</span>
              {kpi.delta && (
                <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full flex items-center gap-0.5 ${style.badge}`}>
                  {kpi.trend === 'positive' ? (
                    <ArrowUpRight className="w-3 h-3" />
                  ) : kpi.trend === 'negative' ? (
                    <ArrowDownRight className="w-3 h-3" />
                  ) : (
                    <Minus className="w-3 h-3" />
                  )}
                  {kpi.delta}
                </span>
              )}
            </div>

            <div className="text-2xl font-bold tracking-tight text-slate-100 my-1">
              {kpi.value}
            </div>

            {kpi.subtitle && (
              <p className="text-xs text-slate-500 mt-1 line-clamp-1">{kpi.subtitle}</p>
            )}
          </div>
        );
      })}
    </div>
  );
};
