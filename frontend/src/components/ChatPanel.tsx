import React, { useState } from 'react';
import { Send, MessageSquare, CornerDownRight, Sparkles } from 'lucide-react';

interface ChatPanelProps {
  history: { role: string; content: string }[];
  onSendMessage: (msg: string) => void;
  isInvestigating: boolean;
}

const SAMPLE_QUESTIONS = [
  "Why did our profits decline in North India last quarter?",
  "Now compare that with the same month last year.",
  "Which routes are causing the highest transportation costs?",
  "Did weather conditions affect deliveries or spoilage?",
  "Calculate the estimated financial loss and suggest what we should do next.",
  "Which product saw volume growth but a drop in profit margins in 2024?"
];

export const ChatPanel: React.FC<ChatPanelProps> = ({ history, onSendMessage, isInvestigating }) => {
  const [text, setText] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim() || isInvestigating) return;
    onSendMessage(text.trim());
    setText('');
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col h-full max-h-[750px]">
      <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <MessageSquare className="w-4 h-4 text-blue-400" />
          <h3 className="font-semibold text-sm text-slate-100">Executive Dialogue</h3>
        </div>
        <span className="text-[10px] text-slate-400">Context Preserved</span>
      </div>

      {/* Suggested Follow-up Questions Pills */}
      <div className="mb-3 space-y-1.5">
        <span className="text-[10px] text-slate-500 uppercase font-semibold flex items-center gap-1">
          <Sparkles className="w-3 h-3 text-indigo-400" />
          Suggested Business Inquiries:
        </span>
        <div className="flex flex-wrap gap-1.5">
          {SAMPLE_QUESTIONS.map((q, idx) => (
            <button
              key={idx}
              onClick={() => onSendMessage(q)}
              disabled={isInvestigating}
              className="text-left text-[11px] px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-blue-600/20 hover:border-blue-500/40 border border-slate-700/60 text-slate-300 transition text-ellipsis overflow-hidden"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* Chat Messages Log */}
      <div className="flex-1 overflow-y-auto space-y-3 pr-1 my-2">
        {history.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-6 text-slate-500">
            <MessageSquare className="w-8 h-8 mb-2 opacity-40 text-blue-400" />
            <p className="text-xs">No prior inquiries in this session.</p>
            <p className="text-[11px] text-slate-600 mt-1">Tap the microphone or select a prompt above to start.</p>
          </div>
        ) : (
          history.map((msg, idx) => {
            const isUser = msg.role === 'user';
            return (
              <div
                key={idx}
                className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}
              >
                <span className="text-[10px] text-slate-500 mb-0.5 px-1 font-medium">
                  {isUser ? 'You (Voice/Text)' : 'FreshRoute BI Agent'}
                </span>
                <div
                  className={`p-3 rounded-xl text-xs max-w-[90%] leading-relaxed ${
                    isUser
                      ? 'bg-blue-600 text-white rounded-br-none shadow-md shadow-blue-500/10'
                      : 'bg-slate-950 border border-slate-800 text-slate-200 rounded-bl-none shadow-sm'
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Text Message Input */}
      <form onSubmit={handleSubmit} className="mt-3 pt-2 border-t border-slate-800 flex items-center gap-2">
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Ask or follow up on your business..."
          disabled={isInvestigating}
          className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
        />
        <button
          type="submit"
          disabled={!text.trim() || isInvestigating}
          className="p-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white disabled:opacity-50 transition active:scale-95 shadow-md shadow-blue-500/20"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
};
