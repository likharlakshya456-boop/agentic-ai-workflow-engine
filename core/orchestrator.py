"""
Multi-Agent Orchestrator
Coordinates dynamic execution graphs (DAGs), state sharing, and task dispatching across agents.
"""
from typing import Dict, Any, List, Optional
import time
import logging
from .agent import BaseAgent

logger = logging.getLogger("Orchestrator")

class WorkflowOrchestrator:
    def __init__(self, workflow_name: str = "EnterpriseAgenticPipeline"):
        self.workflow_name = workflow_name
        self.agents: Dict[str, BaseAgent] = {}
        self.execution_log: List[Dict[str, Any]] = []

    def register_agent(self, agent: BaseAgent):
        self.agents[agent.name] = agent
        logger.info(f"Orchestrator registered agent: {agent.name} ({agent.role})")

    def run_pipeline(self, initial_goal: str, input_payload: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.time()
        logger.info(f"Starting pipeline '{self.workflow_name}' with goal: {initial_goal}")
        
        context = {
            "initial_goal": initial_goal,
            "inputs": input_payload,
            "artifacts": {},
            "step_results": {}
        }

        # Step 1: Research & Discovery
        if "researcher" in self.agents:
            res_agent = self.agents["researcher"]
            logger.info("Dispatching task to Researcher...")
            res_output = res_agent.execute_tool(
                "query_sources",
                topic=initial_goal,
                scope=input_payload.get("scope", "broad")
            )
            context["step_results"]["research"] = res_output
            context["artifacts"]["research_findings"] = res_output.get("summary")

        # Step 2: Data Analysis & Metrics
        if "analyst" in self.agents:
            ana_agent = self.agents["analyst"]
            logger.info("Dispatching task to Analyst...")
            ana_output = ana_agent.execute_tool(
                "analyze_dataset",
                data=context["step_results"].get("research", {}).get("raw_data", [])
            )
            context["step_results"]["analysis"] = ana_output
            context["artifacts"]["metrics"] = ana_output.get("metrics")

        # Step 3: Code Review / Synthesis
        if "code_reviewer" in self.agents:
            coder_agent = self.agents["code_reviewer"]
            logger.info("Dispatching task to Code Reviewer...")
            code_output = coder_agent.execute_tool(
                "audit_and_generate",
                specs=context["artifacts"]
            )
            context["step_results"]["code_review"] = code_output
            context["artifacts"]["final_code_patch"] = code_output.get("patch")

        duration = round(time.time() - start_time, 3)
        summary = {
            "workflow": self.workflow_name,
            "status": "COMPLETED_SUCCESSFULLY",
            "duration_sec": duration,
            "steps_executed": list(context["step_results"].keys()),
            "artifacts_count": len(context["artifacts"]),
            "final_context": context
        }
        self.execution_log.append(summary)
        return summary
