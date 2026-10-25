import React, { useState, useEffect } from 'react';
import { WorkspaceState, VoiceState } from './types';
import { api } from './services/api';
import { Header } from './components/Header';
import { WorkspaceCanvas } from './components/WorkspaceCanvas';
import { ChatPanel } from './components/ChatPanel';
import { TranscriptModal } from './components/TranscriptModal';
import { Loader2 } from 'lucide-react';

export const App: React.FC = () => {
  const [workspace, setWorkspace] = useState<WorkspaceState | null>(null);
  const [voiceState, setVoiceState] = useState<VoiceState>('idle');
  const [pendingTranscript, setPendingTranscript] = useState<string>('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoadingInitial, setIsLoadingInitial] = useState(true);

  // Load baseline starter investigation on startup
  useEffect(() => {
    async function init() {
      try {
        const initial = await api.getInitialWorkspace();
        setWorkspace(initial);
      } catch (err) {
        console.error('Failed to load initial workspace', err);
      } finally {
        setIsLoadingInitial(false);
      }
    }
    init();
  }, []);

  const handleTranscriptReady = (transcript: string) => {
    setPendingTranscript(transcript);
    setVoiceState('confirming');
    setIsModalOpen(true);
  };

  const handleConfirmTranscript = async (finalTranscript: string) => {
    setIsModalOpen(false);
    await executeInvestigation(finalTranscript);
  };

  const executeInvestigation = async (query: string) => {
    setVoiceState('investigating');
    try {
      const history = workspace?.conversation_history || [];
      const updated = await api.investigateQuery(query, history);
      setWorkspace(updated);
      setVoiceState(updated.spoken_response ? 'speaking' : 'idle');
    } catch (err: any) {
      alert(`Investigation Error: ${err.message || err}`);
      setVoiceState('idle');
    }
  };

  if (isLoadingInitial) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center text-slate-400 gap-3">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
        <span className="text-sm font-medium">Initializing FreshRoute Voice BI Workspace...</span>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Header />

      <main className="flex-1 max-w-7xl w-full mx-auto p-4 lg:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Main Collaborative Analytics Workspace Canvas (8 cols on lg) */}
        <div className="lg:col-span-8">
          {workspace && (
            <WorkspaceCanvas
              workspace={workspace}
              voiceState={voiceState}
              onTranscriptReady={handleTranscriptReady}
              onVoiceStateChange={setVoiceState}
            />
          )}
        </div>

        {/* Executive Dialogue & Follow-up Panel (4 cols on lg) */}
        <div className="lg:col-span-4">
          <div className="sticky top-20">
            <ChatPanel
              history={workspace?.conversation_history || []}
              onSendMessage={executeInvestigation}
              isInvestigating={voiceState === 'investigating'}
            />
          </div>
        </div>
      </main>

      {/* Transcript Review Modal */}
      <TranscriptModal
        isOpen={isModalOpen}
        initialTranscript={pendingTranscript}
        onConfirm={handleConfirmTranscript}
        onCancel={() => {
          setIsModalOpen(false);
          setVoiceState('idle');
        }}
      />
    </div>
  );
};

export default App;
