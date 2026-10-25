import { WorkspaceState } from '../types';

const API_BASE = '/api';

export const api = {
  async getInitialWorkspace(): Promise<WorkspaceState> {
    const res = await fetch(`${API_BASE}/workspace/initial`);
    if (!res.ok) throw new Error('Failed to load initial workspace');
    return res.json();
  },

  async investigateQuery(query: string, conversationHistory: { role: string; content: string }[] = []): Promise<WorkspaceState> {
    const res = await fetch(`${API_BASE}/chat/investigate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, conversation_history: conversationHistory })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Investigation failed' }));
      throw new Error(err.detail || 'Investigation failed');
    }
    return res.json();
  },

  async transcribeAudio(audioBlob: Blob): Promise<{ transcript: string; confidence: number; provider: string }> {
    const formData = new FormData();
    formData.append('file', audioBlob, 'voice_query.wav');
    const res = await fetch(`${API_BASE}/voice/transcribe`, {
      method: 'POST',
      body: formData
    });
    if (!res.ok) throw new Error('Audio transcription failed');
    return res.json();
  },

  async synthesizeSpeech(text: string, voice = 'en-IN-female-1'): Promise<{ audio_base64?: string; text: string; client_speech_fallback: boolean }> {
    const res = await fetch(`${API_BASE}/voice/synthesize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, voice })
    });
    if (!res.ok) throw new Error('Speech synthesis failed');
    return res.json();
  },

  async runSQL(query: string): Promise<any> {
    const res = await fetch(`${API_BASE}/workspace/sql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });
    return res.json();
  }
};
