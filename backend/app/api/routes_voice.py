from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.app.gnani_adapters.prisma_stt import prisma_stt_provider
from backend.app.gnani_adapters.timbre_tts import timbre_tts_provider

router = APIRouter(prefix="/api/voice", tags=["Voice Interaction"])

class SynthesizeRequest(BaseModel):
    text: str
    voice: Optional[str] = "Aarohi"

@router.post("/transcribe")
async def transcribe_audio(
    file: Optional[UploadFile] = File(None),
    audio_base64: Optional[str] = Form(None)
):
    """Transcribes audio using Gnani.ai Prisma v2.5 STT."""
    audio_bytes = b""
    audio_fmt = "wav"

    if file:
        audio_bytes = await file.read()
        if file.filename and "." in file.filename:
            audio_fmt = file.filename.split(".")[-1].lower()
    elif audio_base64:
        import base64
        try:
            # Handle possible data URL prefix
            if "base64," in audio_base64:
                audio_base64 = audio_base64.split("base64,")[1]
            audio_bytes = base64.b64decode(audio_base64)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid base64 audio payload")
    else:
        raise HTTPException(status_code=400, detail="No audio file or base64 data provided")

    result = await prisma_stt_provider.transcribe_audio(audio_bytes, audio_format=audio_fmt)
    return result

@router.post("/synthesize")
async def synthesize_speech(request: SynthesizeRequest):
    """Synthesizes text using Gnani.ai Timbre v2.5 TTS."""
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    result = await timbre_tts_provider.synthesize_speech(request.text, voice=request.voice or "default")
    return result
