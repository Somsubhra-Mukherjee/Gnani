import React from 'react';
import { DataTable } from '../types';
import { Table as TableIcon } from 'lucide-react';

interface DataTableSectionProps {
  tables: DataTable[];
}

export const DataTableSection: React.FC<DataTableSectionProps> = ({ tables }) => {
  if (!tables || tables.length === 0) return null;

  return (
    <div className="space-y-5 my-5">
      {tables.map((tbl) => (
        <div key={tbl.table_id} className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg">
          <div className="flex items-center gap-2 pb-3 mb-3 border-b border-slate-800">
            <TableIcon className="w-4 h-4 text-blue-400" />
            <h3 className="font-semibold text-sm text-slate-100">{tbl.title}</h3>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950/70 text-slate-400 uppercase tracking-wider text-[10px]">
                <tr>
                  {tbl.columns.map((col, idx) => (
                    <th key={idx} className="py-2.5 px-3 font-semibold border-b border-slate-800">
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-200">
                {tbl.rows.map((row, rIdx) => (
                  <tr key={rIdx} className="hover:bg-slate-800/40 transition">
                    {tbl.columns.map((col, cIdx) => (
                      <td key={cIdx} className="py-2.5 px-3">
                        {row[col] ?? '-'}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}
    </div>
  );
};
