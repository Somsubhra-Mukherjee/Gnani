import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "FreshRoute" in data["app_name"]

def test_chat_investigate_endpoint():
    payload = {
        "query": "Which routes are causing the highest transportation costs?",
        "conversation_history": []
    }
    response = client.post("/api/chat/investigate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "kpis" in data
    assert "charts" in data
    assert "evidence" in data
    assert data["current_status"] == "completed"

def test_voice_transcribe_endpoint():
    # Pass dummy base64 audio
    import base64
    fake_audio = base64.b64encode(b"RIFF" + b"\x00" * 100).decode('utf-8')
    response = client.post("/api/voice/transcribe", data={"audio_base64": fake_audio})
    assert response.status_code == 200
    data = response.json()
    assert "transcript" in data
    assert data["confidence"] > 0.9

def test_voice_synthesize_endpoint():
    payload = {"text": "Profit fell by 50 Lakh rupees."}
    response = client.post("/api/voice/synthesize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "audio_base64" in data

def test_sql_console_endpoint():
    payload = {"query": "SELECT COUNT(*) as c FROM regions;"}
    response = client.post("/api/workspace/sql", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["rows"][0]["c"] == 5

def test_sql_console_blocks_delete():
    payload = {"query": "DELETE FROM regions;"}
    response = client.post("/api/workspace/sql", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "Security Validation Rejected" in data["error"]
