"""
Core Base Agent for Wolfram CAG Framework
Enforces strict Computation-Augmented Generation (CAG) rules:
For any calculation involving topology, astrophysics, unit conversion, or dimensional analysis,
the agent formulates deterministic code and executes it via Wolfram MCP / Python tools.
"""

from typing import Dict, Any

class BaseCAGAgent:
    def __init__(self, name: str, strict_cag_mode: bool = True):
        self.name = name
        self.strict_cag_mode = strict_cag_mode

    def format_cag_system_prompt(self) -> str:
        return (
            f"You are {self.name}, operating under strict CAG (Computation-Augmented Generation).\n"
            "SYSTEM RULE: You MUST NEVER perform mathematical, dimensional, or cosmological "
            "calculations in pure text/LLM parameters. You MUST formulate deterministic Wolfram Language "
            "or Python executable blocks and evaluate them via the MCP tools."
        )

    def route_query(self, query: str) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement route_query")
