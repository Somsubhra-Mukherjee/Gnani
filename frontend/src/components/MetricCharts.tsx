import React, { useState } from 'react';
import { ChartConfig } from '../types';
import { BarChart3, LineChart as LineChartIcon } from 'lucide-react';

interface MetricChartsProps {
  charts: ChartConfig[];
}

export const MetricCharts: React.FC<MetricChartsProps> = ({ charts }) => {
  if (!charts || charts.length === 0) return null;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 my-5">
      {charts.map((chart) => (
        <ChartCard key={chart.chart_id} chart={chart} />
      ))}
    </div>
  );
};

const ChartCard: React.FC<{ chart: ChartConfig }> = ({ chart }) => {
  const [hoveredIdx, setHoveredIdx] = useState<number | null>(null);

  const data = chart.data;
  if (!data || data.length === 0) return null;

  const isBar = chart.chart_type === 'bar';
  const series = chart.series;

  // Calculate min and max for scaling
  let minVal = 0;
  let maxVal = -Infinity;

  data.forEach((d) => {
    series.forEach((s) => {
      const val = Number(d[s.data_key] ?? 0);
      if (val < minVal) minVal = val;
      if (val > maxVal) maxVal = val;
    });
  });

  if (maxVal === -Infinity) maxVal = 100;
  if (minVal > 0) minVal = 0;
  const range = maxVal - minVal || 1;

  const chartHeight = 220;
  const chartWidth = 500;
  const paddingX = 40;
  const paddingY = 25;
  const innerHeight = chartHeight - paddingY * 2;
  const innerWidth = chartWidth - paddingX * 2;

  const getY = (val: number) => {
    return paddingY + innerHeight - ((val - minVal) / range) * innerHeight;
  };

  const getX = (idx: number) => {
    return paddingX + (idx / Math.max(data.length - 1, 1)) * innerWidth;
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
      <div className="flex items-center justify-between pb-3 mb-2 border-b border-slate-800/80">
        <div className="flex items-center gap-2">
          {isBar ? (
            <BarChart3 className="w-4 h-4 text-blue-400" />
          ) : (
            <LineChartIcon className="w-4 h-4 text-indigo-400" />
          )}
          <h3 className="font-semibold text-sm text-slate-100">{chart.title}</h3>
        </div>
        <div className="flex items-center gap-3 text-xs">
          {series.map((s) => (
            <div key={s.data_key} className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: s.color }}></span>
              <span className="text-slate-400 text-[11px]">{s.name}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="relative w-full overflow-x-auto py-2">
        <svg viewBox={`0 0 ${chartWidth} ${chartHeight}`} className="w-full h-auto overflow-visible">
          {/* Zero Line if negative values exist */}
          {minVal < 0 && (
            <line
              x1={paddingX}
              y1={getY(0)}
              x2={chartWidth - paddingX}
              y2={getY(0)}
              stroke="#64748B"
              strokeDasharray="4 4"
              strokeWidth="1"
            />
          )}

          {/* Grid lines */}
          {[0, 0.5, 1].map((pct) => {
            const v = minVal + pct * range;
            const y = getY(v);
            return (
              <g key={pct}>
                <line
                  x1={paddingX}
                  y1={y}
                  x2={chartWidth - paddingX}
                  y2={y}
                  stroke="#334155"
                  strokeDasharray="2 4"
                  strokeWidth="0.75"
                />
                <text x={paddingX - 6} y={y + 3} textAnchor="end" fill="#64748B" fontSize="9">
                  {Math.round(v)}
                </text>
              </g>
            );
          })}

          {/* Bar Chart Rendering */}
          {isBar &&
            data.map((d, dIdx) => {
              const groupWidth = innerWidth / data.length;
              const barWidth = Math.min(groupWidth / (series.length + 0.5), 18);
              const groupX = paddingX + dIdx * groupWidth + (groupWidth - barWidth * series.length) / 2;

              return (
                <g key={dIdx} onMouseEnter={() => setHoveredIdx(dIdx)} onMouseLeave={() => setHoveredIdx(null)}>
                  {series.map((s, sIdx) => {
                    const val = Number(d[s.data_key] ?? 0);
                    const y0 = getY(0);
                    const yVal = getY(val);
                    const barY = val >= 0 ? yVal : y0;
                    const barH = Math.abs(y0 - yVal) || 2;
                    const bx = groupX + sIdx * barWidth;

                    return (
                      <rect
                        key={s.data_key}
                        x={bx}
                        y={barY}
                        width={barWidth - 2}
                        height={barH}
                        rx="2"
                        fill={s.color}
                        opacity={hoveredIdx === null || hoveredIdx === dIdx ? 0.9 : 0.4}
                        className="transition-all duration-150 cursor-pointer"
                      />
                    );
                  })}
                  <text
                    x={paddingX + (dIdx + 0.5) * groupWidth}
                    y={chartHeight - 6}
                    textAnchor="middle"
                    fill="#94A3B8"
                    fontSize="10"
                    fontWeight="500"
                  >
                    {d[chart.x_axis_key]}
                  </text>
                </g>
              );
            })}

          {/* Line Chart Rendering */}
          {!isBar && (
            <>
              {series.map((s) => {
                const points = data
                  .map((d, idx) => `${getX(idx)},${getY(Number(d[s.data_key] ?? 0))}`)
                  .join(' ');

                return (
                  <g key={s.data_key}>
                    <polyline
                      fill="none"
                      stroke={s.color}
                      strokeWidth="2.5"
                      points={points}
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                    {data.map((d, idx) => {
                      const cx = getX(idx);
                      const cy = getY(Number(d[s.data_key] ?? 0));
                      const isHov = hoveredIdx === idx;
                      return (
                        <circle
                          key={idx}
                          cx={cx}
                          cy={cy}
                          r={isHov ? 5 : 3}
                          fill={s.color}
                          stroke="#0F172A"
                          strokeWidth="2"
                          onMouseEnter={() => setHoveredIdx(idx)}
                          onMouseLeave={() => setHoveredIdx(null)}
                          className="cursor-pointer transition-all"
                        />
                      );
                    })}
                  </g>
                );
              })}

              {/* X Axis Labels for Line */}
              {data.map((d, idx) => (
                <text
                  key={idx}
                  x={getX(idx)}
                  y={chartHeight - 6}
                  textAnchor="middle"
                  fill="#94A3B8"
                  fontSize="10"
                  fontWeight="500"
                >
                  {d[chart.x_axis_key]}
                </text>
              ))}
            </>
          )}
        </svg>

        {/* Hover Tooltip display */}
        {hoveredIdx !== null && data[hoveredIdx] && (
          <div className="mt-2 p-2.5 rounded-lg bg-slate-950/90 border border-slate-700/80 text-xs flex items-center justify-between">
            <span className="font-semibold text-slate-200">
              {data[hoveredIdx][chart.x_axis_key]}:
            </span>
            <div className="flex items-center gap-3">
              {series.map((s) => (
                <span key={s.data_key} className="flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: s.color }}></span>
                  <span className="text-slate-400">{s.name}:</span>
                  <strong className="text-slate-100">{data[hoveredIdx][s.data_key]}</strong>
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
