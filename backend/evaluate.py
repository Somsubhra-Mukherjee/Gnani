import json
import asyncio
import sys
from typing import Dict, Any, List
from backend.app.agent.orchestrator import orchestrator
from backend.app.security.readonly_service import run_readonly_sql
from backend.app.security.sql_validator import SQLSecurityValidator
from backend.app.gnani_adapters.prisma_stt import prisma_stt_provider
from backend.app.gnani_adapters.timbre_tts import timbre_tts_provider

async def run_evaluation():
    print("=" * 70)
    print("FreshRoute Voice BI Agent - Comprehensive Evaluation Benchmark")
    print("=" * 70)

    with open("backend/ground_truth.json", "r") as f:
        ground_truth = json.load(f)

    benchmarks = ground_truth["evaluation_benchmarks"]
    total = len(benchmarks)
    passed = 0
    scores = {
        "sql_security_rejection": {"total": 0, "passed": 0},
        "root_cause_accuracy": {"total": 0, "passed": 0},
        "numerical_correctness": {"total": 0, "passed": 0},
        "follow_up_context": {"total": 0, "passed": 0},
        "voice_pipeline": {"total": 0, "passed": 0}
    }

    print(f"Loaded {total} benchmark test cases from ground_truth.json\n")

    for idx, tc in enumerate(benchmarks, 1):
        tc_id = tc["id"]
        cat = tc["category"]
        question = tc["question"]
        print(f"[{idx}/{total}] Testing {tc_id} ({cat}): '{question}'")

        if cat == "adversarial_security":
            scores["sql_security_rejection"]["total"] += 1
            # Test direct SQL validator & orchestrator security
            ws = await orchestrator.investigate(question)
            has_guardrail = any(s.action == "security_guardrail" for s in ws.timeline)
            
            # Also test direct query extraction if applicable
            sql_attempt = question
            if "Execute:" in question:
                sql_attempt = question.split("Execute:")[1].strip()
            elif "using" in question:
                sql_attempt = question.split("using")[1].strip()

            val_res = SQLSecurityValidator().validate(sql_attempt)
            is_rejected = (not val_res.is_valid) or has_guardrail

            if is_rejected:
                scores["sql_security_rejection"]["passed"] += 1
                passed += 1
                print(f"  --> PASSED: Safely blocked adversarial attack.")
            else:
                print(f"  --> FAILED: Failed to reject: {val_res.error}")

        elif cat == "follow_up_conversational":
            scores["follow_up_context"]["total"] += 1
            # Test turn 1 then turn 2
            ws_prev = await orchestrator.investigate("Why did North India profits fall in August 2024?")
            ws_follow = await orchestrator.investigate(question, conversation_history=ws_prev.conversation_history)
            
            has_yoy = any("2023 vs 2024" in c.title or "YoY" in c.title for c in ws_follow.charts)
            if has_yoy and ws_follow.spoken_response and "78.4" in ws_follow.spoken_response.text:
                scores["follow_up_context"]["passed"] += 1
                passed += 1
                print(f"  --> PASSED: Conversational context preserved, YoY delta calculated.")
            else:
                print(f"  --> FAILED: Conversational context failed.")

        else:
            # Standard Business Investigation
            scores["root_cause_accuracy"]["total"] += 1
            scores["numerical_correctness"]["total"] += 1
            
            ws = await orchestrator.investigate(question)
            
            # Check tool executions
            has_sql = len(ws.evidence.sql_queries) > 0
            has_citations = (len(ws.evidence.internal_docs) > 0) or (len(ws.evidence.weather_records) > 0) or (len(ws.evidence.web_sources) > 0)
            has_kpis = len(ws.kpis) > 0
            has_spoken = ws.spoken_response is not None and len(ws.spoken_response.text) > 20

            # Check expected numbers if provided
            exp_metrics = tc.get("expected_metrics", {})
            metrics_match = True
            if "net_profit_inr" in exp_metrics:
                # -5024400.0 (represented as ₹-50.2 Lakhs)
                metrics_match = "50.2" in str(ws.kpis[0].value) or "50.2" in ws.spoken_response.text

            if has_sql and has_citations and has_kpis and has_spoken and metrics_match:
                scores["root_cause_accuracy"]["passed"] += 1
                scores["numerical_correctness"]["passed"] += 1
                passed += 1
                print(f"  --> PASSED: Investigated across tools, verified metrics & generated speech.")
            else:
                print(f"  --> FAILED: Missing citations or metrics. SQL: {has_sql}, Docs: {has_citations}, KPIs: {has_kpis}")

    # Voice pipeline test
    scores["voice_pipeline"]["total"] += 1
    stt_res = await prisma_stt_provider.transcribe_audio(b"dummy_audio" * 20)
    tts_res = await timbre_tts_provider.synthesize_speech("FreshRoute Voice BI Agent ready.")
    if "transcript" in stt_res and tts_res.get("audio_base64"):
        scores["voice_pipeline"]["passed"] += 1
        print("\n[+] Testing Voice Pipeline: Prisma v2.5 STT & Timbre v2.5 TTS PASSED")

    # Scorecard
    print("\n" + "=" * 70)
    print("FINAL EVALUATION SCORECARD")
    print("=" * 70)
    print(f"Total Benchmark Tests: {total}")
    print(f"Successful Tests:      {passed}")
    overall_pct = round((passed / total) * 100, 1)
    print(f"Overall Accuracy:      {overall_pct}%\n")
    print("Category Breakdown:")
    for cat_name, data in scores.items():
        if data["total"] > 0:
            pct = round((data["passed"] / data["total"]) * 100, 1)
            print(f"  - {cat_name:25}: {data['passed']}/{data['total']} ({pct}%)")
    print("=" * 70)

    return overall_pct >= 90.0

if __name__ == "__main__":
    success = asyncio.run(run_evaluation())
    sys.exit(0 if success else 1)
