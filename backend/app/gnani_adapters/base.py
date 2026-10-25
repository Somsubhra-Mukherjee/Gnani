from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseSTTProvider(ABC):
    @abstractmethod
    async def transcribe_audio(self, audio_bytes: bytes, audio_format: str = "wav") -> Dict[str, Any]:
        """Transcribes incoming speech audio to text transcript."""
        pass

class BaseTTSProvider(ABC):
    @abstractmethod
    async def synthesize_speech(self, text: str, voice: str = "default") -> Dict[str, Any]:
        """Synthesizes text into spoken audio stream/base64."""
        pass

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        system_prompt: str,
        tools: Optional[List[Dict[str, Any]]] = None,
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Generates reasoning response or structured tool-call proposals."""
        pass
