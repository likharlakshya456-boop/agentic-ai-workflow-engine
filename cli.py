"""
Interactive CLI for Autonomous Multi-Agent AI Workflow Engine
"""
import sys
import os
import json
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.orchestrator import WorkflowOrchestrator
from agents.researcher import ResearcherAgent
from agents.data_analyst import DataAnalystAgent
from agents.code_reviewer import CodeReviewerAgent

def run_cli():
    print("=" * 65)
    print("🚀 AUTONOMOUS MULTI-AGENT AI WORKFLOW ENGINE v1.0.0")
    print("Author: Lakshya Likhar (@likharlakshya456-boop)")
    print("=" * 65)
    
    orchestrator = WorkflowOrchestrator("ProductionPipeline")
    orchestrator.register_agent(ResearcherAgent())
    orchestrator.register_agent(DataAnalystAgent())
    orchestrator.register_agent(CodeReviewerAgent())

    goal = sys.argv[1] if len(sys.argv) > 1 else "Chromium Multi-Process Telemetry Integration"
    print(f"\n[GOAL] {goal}")
    print("\n[DISPATCHING] Initializing autonomous agents...")
    time.sleep(0.5)

    result = orchestrator.run_pipeline(
        initial_goal=goal,
        input_payload={"scope": "systems_architecture", "priority": "high"}
    )

    print("\n" + "=" * 65)
    print(f"✅ PIPELINE FINISHED: {result['status']}")
    print(f"⏱️ Duration: {result['duration_sec']}s")
    print(f"📦 Steps Executed: {', '.join(result['steps_executed'])}")
    print(f"📊 Metrics: {result['final_context']['artifacts'].get('metrics')}")
    print(f"🛡️ Audit Grade: {result['final_context']['step_results']['code_review'].get('grade')}")
    print("=" * 65)

if __name__ == "__main__":
    run_cli()
