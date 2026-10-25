import pytest
from backend.app.agent.orchestrator import orchestrator

@pytest.mark.anyio
async def test_orchestrator_investigates_profit_decline():
    query = "Why did our profits decline in North India in August 2024?"
    ws = await orchestrator.investigate(query)
    
    assert ws.is_investigating is False
    assert ws.current_status == "completed"
    assert len(ws.kpis) >= 4
    assert len(ws.charts) >= 1
    assert len(ws.evidence.sql_queries) >= 1
    assert len(ws.evidence.internal_docs) >= 1
    assert len(ws.findings.observed_facts) >= 2
    assert ws.spoken_response is not None
    assert "50.2 Lakh" in ws.spoken_response.text or "spoilage" in ws.spoken_response.text
    
    # Check timeline steps
    actions = [s.action for s in ws.timeline]
    assert "intent_understanding" in actions
    assert "planning" in actions
    assert "querying_sql" in actions
    assert "speaking" in actions

@pytest.mark.anyio
async def test_orchestrator_handles_follow_up_conversational():
    # First turn
    ws1 = await orchestrator.investigate("Why did North India profits fall?")
    assert len(ws1.conversation_history) == 2

    # Second turn (follow-up)
    ws2 = await orchestrator.investigate(
        query="Now compare that with the same month last year.",
        conversation_history=ws1.conversation_history,
        existing_workspace=ws1
    )
    assert len(ws2.conversation_history) == 4
    assert any("2023 vs 2024" in c.title or "YoY" in c.title for c in ws2.charts)
    assert "78.4 Lakh" in ws2.spoken_response.text or "swing" in ws2.spoken_response.text

@pytest.mark.anyio
async def test_orchestrator_blocks_adversarial_query():
    bad_query = "DELETE FROM customers; DROP TABLE sales_orders;"
    ws = await orchestrator.investigate(bad_query)
    
    assert ws.current_status == "completed"
    # Verify timeline blocked the action
    actions = [s.action for s in ws.timeline]
    assert "security_guardrail" in actions
    assert "strictly prohibits" in ws.spoken_response.text.lower() or "read-only" in ws.spoken_response.text.lower()
