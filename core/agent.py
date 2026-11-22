"""
Autonomous Agent Base Class
Provides memory management, tool execution, and lifecycle hooks.
"""
from typing import Dict, Any, List, Callable, Optional
import time
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

class BaseAgent:
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.tools: Dict[str, Callable] = {}
        self.memory: List[Dict[str, Any]] = []
        self.logger = logging.getLogger(self.name)

    def register_tool(self, name: str, tool_func: Callable, description: str = ""):
        self.tools[name] = {
            "func": tool_func,
            "description": description
        }
        self.logger.info(f"Registered tool: {name}")

    def execute_tool(self, name: str, **kwargs) -> Any:
        if name not in self.tools:
            raise ValueError(f"Tool {name} not found in agent {self.name}")
        self.logger.info(f"Executing tool: {name} with args {kwargs}")
        start_time = time.time()
        try:
            result = self.tools[name]["func"](**kwargs)
            duration = time.time() - start_time
            self.memory.append({
                "type": "tool_execution",
                "tool": name,
                "input": kwargs,
                "output": result,
                "duration_sec": round(duration, 3)
            })
            return result
        except Exception as e:
            self.logger.error(f"Error executing {name}: {str(e)}")
            self.memory.append({
                "type": "tool_error",
                "tool": name,
                "error": str(e)
            })
            raise e

    def think_and_plan(self, objective: str) -> List[str]:
        self.logger.info(f"Formulating plan for: {objective}")
        plan = [
            f"1. Deconstruct objective: {objective}",
            "2. Identify required tools and data sources",
            "3. Execute sub-tasks with strict validation",
            "4. Synthesize structured output"
        ]
        self.memory.append({"type": "plan", "objective": objective, "steps": plan})
        return plan

    def summarize_state(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role,
            "tools_count": len(self.tools),
            "memory_items": len(self.memory),
            "recent_actions": self.memory[-3:] if self.memory else []
        }
