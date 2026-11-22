"""
Unit & Integration Tests for Agentic AI Workflow Engine
Compatible with both standard python unittest and pytest.
"""
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.orchestrator import WorkflowOrchestrator
from core.agent import BaseAgent
from agents.researcher import ResearcherAgent
from agents.data_analyst import DataAnalystAgent
from agents.code_reviewer import CodeReviewerAgent

class TestAgenticEngine(unittest.TestCase):
    def test_base_agent_registration(self):
        agent = BaseAgent(name="tester", role="Tester", system_prompt="Test prompt")
        agent.register_tool("echo", lambda text: f"echo:{text}", "Echoes text")
        self.assertIn("echo", agent.tools)
        result = agent.execute_tool("echo", text="hello")
        self.assertEqual(result, "echo:hello")
        self.assertEqual(len(agent.memory), 1)
        self.assertEqual(agent.memory[0]["type"], "tool_execution")

    def test_base_agent_invalid_tool(self):
        agent = BaseAgent(name="tester", role="Tester", system_prompt="Test prompt")
        with self.assertRaises(ValueError) as ctx:
            agent.execute_tool("non_existent_tool")
        self.assertIn("Tool non_existent_tool not found", str(ctx.exception))

    def test_pipeline_execution(self):
        orchestrator = WorkflowOrchestrator("TestPipeline")
        orchestrator.register_agent(ResearcherAgent())
        orchestrator.register_agent(DataAnalystAgent())
        orchestrator.register_agent(CodeReviewerAgent())

        result = orchestrator.run_pipeline(
            initial_goal="Test Goal",
            input_payload={"scope": "unit_test"}
        )

        self.assertEqual(result["status"], "COMPLETED_SUCCESSFULLY")
        self.assertIn("research", result["steps_executed"])
        self.assertIn("analysis", result["steps_executed"])
        self.assertIn("code_review", result["steps_executed"])
        self.assertEqual(result["artifacts_count"], 3)
        self.assertEqual(result["final_context"]["artifacts"]["metrics"]["coverage_pct"], 100.0)

if __name__ == "__main__":
    unittest.main()
