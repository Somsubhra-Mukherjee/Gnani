import React, { useState, useEffect } from 'react';
import { Check, X, Edit3, Sparkles } from 'lucide-react';

interface TranscriptModalProps {
  isOpen: boolean;
  initialTranscript: string;
  onConfirm: (finalTranscript: string) => void;
  onCancel: () => void;
}

export const TranscriptModal: React.FC<TranscriptModalProps> = ({
  isOpen,
  initialTranscript,
  onConfirm,
  onCancel
}) => {
  const [transcript, setTranscript] = useState(initialTranscript);

  useEffect(() => {
    setTranscript(initialTranscript);
  }, [initialTranscript]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl p-6">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-blue-500/10 text-blue-400">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-semibold text-slate-100 text-sm">Recognized Speech</h3>
              <p className="text-xs text-slate-400">Prisma v2.5 Speech-to-Text</p>
            </div>
          </div>
          <button
            onClick={onCancel}
            className="p-1 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="mt-4">
          <label className="text-xs font-medium text-slate-400 mb-1.5 flex items-center gap-1.5">
            <Edit3 className="w-3.5 h-3.5 text-blue-400" />
            Review or edit your question before investigating:
          </label>
          <textarea
            value={transcript}
            onChange={(e) => setTranscript(e.target.value)}
            rows={3}
            className="w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-slate-100 text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition resize-none"
            placeholder="Type or edit your question..."
          />
        </div>

        <div className="mt-5 flex items-center justify-end gap-3">
          <button
            onClick={onCancel}
            className="px-4 py-2 rounded-xl text-xs font-medium text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition"
          >
            Cancel
          </button>
          <button
            onClick={() => onConfirm(transcript)}
            className="flex items-center gap-2 px-5 py-2 rounded-xl text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/20 transition active:scale-95"
          >
            <Check className="w-4 h-4" />
            Confirm & Investigate
          </button>
        </div>
      </div>
    </div>
  );
};
