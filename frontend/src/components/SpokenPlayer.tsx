import React, { useState, useEffect, useRef } from 'react';
import { Volume2, VolumeX, Play, Pause, RotateCcw } from 'lucide-react';
import { SpokenResponse } from '../types';

interface SpokenPlayerProps {
  spokenResponse?: SpokenResponse;
}

export const SpokenPlayer: React.FC<SpokenPlayerProps> = ({ spokenResponse }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (!spokenResponse || !spokenResponse.text) return;

    // Automatically trigger speech playback
    playSpeech();

    return () => {
      stopSpeech();
    };
  }, [spokenResponse]);

  const playSpeech = () => {
    if (!spokenResponse || !spokenResponse.text) return;
    setIsPlaying(true);

    // 1. If base64 audio chime is present from Timbre
    if (spokenResponse.audio_base64 && !isMuted) {
      try {
        const audioSrc = `data:${spokenResponse.audio_format || 'audio/wav'};base64,${spokenResponse.audio_base64}`;
        if (audioRef.current) {
          audioRef.current.src = audioSrc;
          audioRef.current.play().catch(() => {});
        }
      } catch (e) {}
    }

    // 2. Play verbally through Web Speech API if supported & enabled
    if ('speechSynthesis' in window && !isMuted) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(spokenResponse.text);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      utterance.lang = 'en-IN';

      utterance.onend = () => {
        setIsPlaying(false);
      };
      utterance.onerror = () => {
        setIsPlaying(false);
      };

      window.speechSynthesis.speak(utterance);
    } else {
      setTimeout(() => setIsPlaying(false), 4000);
    }
  };

  const stopSpeech = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    if (audioRef.current) {
      audioRef.current.pause();
    }
    setIsPlaying(false);
  };

  const togglePlay = () => {
    if (isPlaying) {
      stopSpeech();
    } else {
      playSpeech();
    }
  };

  const toggleMute = () => {
    setIsMuted(!isMuted);
    if (!isMuted) {
      stopSpeech();
    }
  };

  if (!spokenResponse || !spokenResponse.text) return null;

  return (
    <div className="bg-gradient-to-r from-purple-950/40 via-indigo-950/30 to-slate-900 border border-purple-500/30 rounded-2xl p-4 my-4 shadow-lg">
      <audio ref={audioRef} className="hidden" />

      <div className="flex items-center justify-between pb-2 mb-2 border-b border-purple-500/20">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-purple-500/20 text-purple-300">
            <Volume2 className="w-4 h-4" />
          </div>
          <div>
            <h4 className="font-semibold text-xs text-purple-200">Spoken Verbal Briefing</h4>
            <span className="text-[10px] text-purple-400">Synthesized via Gnani Timbre v2.5</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={toggleMute}
            className={`p-1.5 rounded-lg transition ${
              isMuted ? 'text-red-400 bg-red-500/10' : 'text-purple-300 hover:bg-purple-900/40'
            }`}
            title={isMuted ? 'Unmute' : 'Mute'}
          >
            {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
          </button>
          <button
            onClick={togglePlay}
            className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold shadow transition active:scale-95"
          >
            {isPlaying ? (
              <>
                <Pause className="w-3.5 h-3.5" />
                <span>Pause</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-white" />
                <span>Replay</span>
              </>
            )}
          </button>
        </div>
      </div>

      <p className="text-slate-200 text-sm leading-relaxed italic bg-slate-950/40 p-3 rounded-xl border border-purple-500/10">
        "{spokenResponse.text}"
      </p>
    </div>
  );
};
