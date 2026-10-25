import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Mic, MicOff, Loader2, Sparkles, Volume2, XCircle } from 'lucide-react';
import { VoiceState } from '../types';
import { api } from '../services/api';

interface VoiceControllerProps {
  currentState: VoiceState;
  onTranscriptReady: (transcript: string) => void;
  onStateChange: (state: VoiceState) => void;
}

const MAX_RECORDING_SECONDS = 10; // Safety guardrail: auto-stop after 10s to guarantee mic security

export const VoiceController: React.FC<VoiceControllerProps> = ({
  currentState,
  onTranscriptReady,
  onStateChange
}) => {
  const [recordingSeconds, setRecordingSeconds] = useState(0);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const timerIntervalRef = useRef<any>(null);
  const recognitionRef = useRef<any>(null);
  const liveTranscriptRef = useRef<string>('');

  // Explicitly stops all hardware microphone tracks and speech engines immediately
  const releaseMicrophone = useCallback(() => {
    if (timerIntervalRef.current) {
      clearInterval(timerIntervalRef.current);
      timerIntervalRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => {
        try {
          track.stop();
          track.enabled = false;
        } catch (e) {
          console.warn('Error stopping track:', e);
        }
      });
      streamRef.current = null;
    }
    if (recognitionRef.current) {
      try {
        recognitionRef.current.abort();
      } catch (e) {}
    }
  }, []);

  // Cleanup on unmount - guarantees mic is closed under all circumstances
  useEffect(() => {
    return () => {
      releaseMicrophone();
    };
  }, [releaseMicrophone]);

  const stopRecording = useCallback(() => {
    if (timerIntervalRef.current) {
      clearInterval(timerIntervalRef.current);
      timerIntervalRef.current = null;
    }

    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      try {
        mediaRecorderRef.current.stop();
      } catch (e) {
        releaseMicrophone();
      }
    } else {
      releaseMicrophone();
    }
  }, [releaseMicrophone]);

  // Cancel recording without saving
  const cancelRecording = () => {
    releaseMicrophone();
    audioChunksRef.current = [];
    liveTranscriptRef.current = '';
    onStateChange('idle');
    setRecordingSeconds(0);
  };

  const startRecording = async () => {
    try {
      // Clean up any lingering stream
      releaseMicrophone();
      audioChunksRef.current = [];
      liveTranscriptRef.current = '';

      // Request mic explicitly
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      // Initialize Web Speech API for immediate live transcription
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (SpeechRecognition) {
        try {
          const recognition = new SpeechRecognition();
          recognition.continuous = false;
          recognition.interimResults = true;
          recognition.lang = 'en-IN';

          recognition.onresult = (event: any) => {
            const current = event.results[event.results.length - 1][0].transcript;
            if (current) {
              liveTranscriptRef.current = current;
            }
          };

          recognition.onerror = (e: any) => {
            console.debug('WebSpeech event:', e);
          };

          recognition.onend = () => {
            // WebSpeech ended
          };

          recognition.start();
          recognitionRef.current = recognition;
        } catch (e) {
          console.debug('WebSpeech not available, falling back to backend STT:', e);
        }
      }

      const recorder = new MediaRecorder(stream);

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          audioChunksRef.current.push(e.data);
        }
      };

      recorder.onstop = async () => {
        // ALWAYS release hardware audio tracks first
        releaseMicrophone();

        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        onStateChange('transcribing');

        let recognizedText = liveTranscriptRef.current.trim();

        // Send to Gnani Prisma STT backend
        try {
          const result = await api.transcribeAudio(audioBlob);
          if (result && result.transcript && result.transcript.trim()) {
            recognizedText = result.transcript.trim();
          }
        } catch (err) {
          console.warn('Backend STT failed:', err);
        }

        if (recognizedText) {
          onTranscriptReady(recognizedText);
        } else {
          onStateChange('idle');
          alert('No clear speech was detected. Please click the mic again, or type your question directly in the text box below.');
        }
      };

      mediaRecorderRef.current = recorder;
      recorder.start();
      onStateChange('listening');
      setRecordingSeconds(0);

      // Auto-stop countdown timer
      timerIntervalRef.current = setInterval(() => {
        setRecordingSeconds((prev) => {
          if (prev >= MAX_RECORDING_SECONDS - 1) {
            // Auto stop when limit reached
            stopRecording();
            return MAX_RECORDING_SECONDS;
          }
          return prev + 1;
        });
      }, 1000);

    } catch (err) {
      releaseMicrophone();
      console.warn('Microphone access denied or error:', err);
      onStateChange('idle');
      alert('Microphone access was denied or not available. You can type any question directly in the Executive Dialogue box below.');
    }
  };

  const handleButtonClick = () => {
    if (currentState === 'listening') {
      stopRecording();
    } else if (currentState === 'idle' || currentState === 'speaking') {
      startRecording();
    }
  };

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <div className="relative group flex items-center gap-3">
        {/* Animated Glow rings */}
        {currentState === 'listening' && (
          <>
            <div className="absolute -inset-3 rounded-full bg-red-500/30 animate-ping opacity-75 duration-1000"></div>
            <div className="absolute -inset-1 rounded-full bg-red-600/40 animate-pulse"></div>
          </>
        )}
        {currentState === 'speaking' && (
          <div className="absolute -inset-2 rounded-full bg-purple-500/40 animate-pulse"></div>
        )}
        {currentState === 'investigating' && (
          <div className="absolute -inset-2 rounded-full bg-blue-500/30 animate-spin"></div>
        )}

        {/* Primary Microphone Button */}
        <button
          onClick={handleButtonClick}
          disabled={currentState === 'transcribing' || currentState === 'investigating'}
          className={`relative z-10 flex items-center gap-3 px-8 py-4 rounded-full font-semibold text-base shadow-2xl transition-all duration-300 transform active:scale-95 ${
            currentState === 'listening'
              ? 'bg-gradient-to-r from-red-600 to-rose-600 text-white shadow-red-500/40 animate-pulse'
              : currentState === 'speaking'
              ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-purple-500/30'
              : currentState === 'transcribing' || currentState === 'investigating'
              ? 'bg-slate-800 text-slate-400 border border-slate-700 cursor-wait'
              : 'bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-700 text-white hover:shadow-blue-500/30 hover:shadow-xl hover:scale-105 border border-blue-400/30'
          }`}
        >
          {currentState === 'listening' ? (
            <>
              <MicOff className="w-6 h-6 animate-bounce" />
              <span>
                Recording ({recordingSeconds}s / {MAX_RECORDING_SECONDS}s) - Tap to Stop
              </span>
            </>
          ) : currentState === 'transcribing' ? (
            <>
              <Loader2 className="w-6 h-6 animate-spin text-blue-400" />
              <span>Transcribing Audio (Prisma v2.5)...</span>
            </>
          ) : currentState === 'investigating' ? (
            <>
              <Sparkles className="w-6 h-6 animate-spin text-indigo-400" />
              <span>Investigating Business Evidence...</span>
            </>
          ) : currentState === 'speaking' ? (
            <>
              <Volume2 className="w-6 h-6 animate-pulse text-purple-200" />
              <span>Speaking Findings (Timbre v2.5)</span>
            </>
          ) : (
            <>
              <div className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center">
                <Mic className="w-5 h-5 text-white" />
              </div>
              <span className="tracking-wide">Ask your business</span>
            </>
          )}
        </button>

        {/* Security Cancel Button: Immediately shuts off mic */}
        {currentState === 'listening' && (
          <button
            onClick={cancelRecording}
            title="Cancel and turn off microphone immediately"
            className="relative z-10 p-3 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-600 shadow-lg transition flex items-center gap-1.5 text-xs"
          >
            <XCircle className="w-5 h-5 text-red-400" />
            <span>Cancel</span>
          </button>
        )}
      </div>

      {/* Security notice & subtitle */}
      <p className="mt-2.5 text-xs text-slate-400 flex items-center gap-1.5 text-center">
        {currentState === 'listening' ? (
          <span className="text-red-400 font-medium flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
            Microphone active. Auto-stops in {MAX_RECORDING_SECONDS - recordingSeconds}s for your privacy.
          </span>
        ) : currentState === 'speaking' ? (
          <span className="text-purple-400">Executive audio response playing (Timbre v2.5)</span>
        ) : (
          <span className="text-slate-400">
            Microphone is <strong className="text-emerald-400 font-semibold">OFF</strong>. Click to ask, or type below.
          </span>
        )}
      </p>
    </div>
  );
};
