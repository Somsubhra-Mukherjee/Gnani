import base64
import logging
import io
import wave
import math
import struct
from typing import Dict, Any, Optional
import httpx
from backend.app.config import settings
from backend.app.gnani_adapters.base import BaseTTSProvider

logger = logging.getLogger("FreshRoute.TimbreTTS")

class GnaniTimbreTTSProvider(BaseTTSProvider):
    """
    Adapter for Gnani.ai Timbre v2.5 Text-to-Speech Model (Vachana Platform).
    Synthesizes executive audio with verified voices (e.g. Aarohi, Nalini, Bhavna).
    Provides safe synthesized WAV tone fallback when offline.
    """
    def __init__(self):
        self.api_key = settings.GNANI_API_KEY
        self.endpoint = settings.GNANI_TIMBRE_ENDPOINT or "https://api.vachana.ai/api/v1/tts/inference"
        self.model_name = settings.GNANI_TTS_MODEL or "timbre-v2.5"
        self.is_mock = not bool(self.api_key)

        if self.is_mock:
            logger.info("Timbre v2.5 initialized in MOCK / DEVELOPMENT mode (No GNANI_API_KEY detected).")
        else:
            logger.info(f"Timbre v2.5 initialized with endpoint: {self.endpoint}")

    def _generate_synthetic_tone_wav(self, duration_sec: float = 1.0) -> bytes:
        """Generates a pleasant harmonic bell chime in WAV format."""
        sample_rate = 16000
        n_samples = int(sample_rate * duration_sec)
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            frames = bytearray()
            for i in range(n_samples):
                decay = math.exp(-3.0 * i / sample_rate)
                val1 = math.sin(2.0 * math.pi * 523.25 * i / sample_rate)  # C5
                val2 = 0.5 * math.sin(2.0 * math.pi * 659.25 * i / sample_rate)  # E5
                sample = int((val1 + val2) * 12000 * decay)
                sample = max(-32767, min(32767, sample))
                frames.extend(struct.pack('<h', sample))
            wav_file.writeframes(frames)
        return buf.getvalue()

    async def synthesize_speech(self, text: str, voice: str = "Aarohi") -> Dict[str, Any]:
        if not text or not text.strip():
            return {"error": "Empty text provided for synthesis", "audio_base64": None}

        # Truncate overly long spoken text for fast low-latency audio delivery
        spoken_text = text.strip()
        if len(spoken_text) > 400:
            spoken_text = spoken_text[:400] + "..."

        if not self.is_mock:
            try:
                async with httpx.AsyncClient(timeout=20.0) as client:
                    headers = {
                        "X-API-Key-ID": self.api_key,
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                    }
                    payload = {
                        "model": "timbre-v2.5",
                        "text": spoken_text,
                        "voice": "Aarohi",
                        "audio_config": {
                            "container": "mp3"
                        }
                    }
                    response = await client.post(
                        self.endpoint,
                        json=payload,
                        headers=headers
                    )
                    if response.status_code == 200 and response.content:
                        audio_b64 = base64.b64encode(response.content).decode("utf-8")
                        return {
                            "audio_base64": f"data:audio/mp3;base64,{audio_b64}",
                            "format": "mp3",
                            "audio_format": "mp3",
                            "voice": "Aarohi (en-IN)",
                            "provider": "Gnani.ai Timbre v2.5 (Live Vachana)",
                            "text": spoken_text
                        }
                    else:
                        logger.warning(f"Gnani Timbre API returned {response.status_code}: {response.text}")
            except Exception as e:
                logger.error(f"Gnani Timbre v2.5 live API failed: {str(e)}. Falling back to local synthesizer.")

        # Local harmonic chime fallback
        tone_wav = self._generate_synthetic_tone_wav(1.0)
        audio_b64 = base64.b64encode(tone_wav).decode("utf-8")
        return {
            "audio_base64": f"data:audio/wav;base64,{audio_b64}",
            "format": "wav",
            "audio_format": "wav",
            "voice": voice,
            "provider": "Gnani.ai Timbre v2.5 (Local Synthesizer Fallback)",
            "text": spoken_text,
            "note": "Audio generated via local synthesizer. Web Speech API browser TTS will read full text verbally."
        }

timbre_tts_provider = GnaniTimbreTTSProvider()
