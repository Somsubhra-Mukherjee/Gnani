import pytest
from backend.app.gnani_adapters.prisma_stt import prisma_stt_provider
from backend.app.gnani_adapters.timbre_tts import timbre_tts_provider
from backend.app.gnani_adapters.evon_llm import evon_llm_provider

@pytest.mark.anyio
async def test_prisma_stt_transcription():
    # Test with dummy audio bytes
    fake_audio = b"RIFF....WAVEfmt ...." * 50
    res = await prisma_stt_provider.transcribe_audio(fake_audio, audio_format="wav")
    assert "transcript" in res
    assert res["confidence"] > 0.9
    assert "Prisma v2.5" in res["provider"]

@pytest.mark.anyio
async def test_timbre_tts_synthesis():
    text = "Our North India operating profit was lowest in August 2024."
    res = await timbre_tts_provider.synthesize_speech(text)
    assert res["audio_base64"] is not None
    assert "Timbre v2.5" in res["provider"]
    assert res["audio_format"] == "wav"

@pytest.mark.anyio
async def test_evon_llm_tool_generation():
    prompt = "Why did our profits decline in North India last quarter?"
    res = await evon_llm_provider.generate_response(prompt=prompt, system_prompt="You are a BI agent.")
    assert len(res["tool_calls"]) > 0
    tool_names = [tc["name"] for tc in res["tool_calls"]]
    assert "run_readonly_sql" in tool_names
    assert "retrieve_company_docs" in tool_names
    assert "Evon v3.3" in res["provider"]
