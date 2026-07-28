"""
Cosmology Agent
Formulates astrophysical queries, dark energy vacuum expansion rates,
and Oligon dark matter density calculations using Wolfram CAG tools.
"""

from agents.core.base_agent import BaseCAGAgent
from mcp.tools.evaluate_symbolic import SymbolicEvaluator
from mcp.tools.unit_manager import UnitManager
from mcp.tools.cosmology_data import CosmologyDataTool

class CosmologyAgent(BaseCAGAgent):
    def __init__(self, strict_cag_mode: bool = True):
        super().__init__(name="CosmologyAgent", strict_cag_mode=strict_cag_mode)
        self.evaluator = SymbolicEvaluator()
        self.unit_mgr = UnitManager()
        self.data_tool = CosmologyDataTool()

    def route_query(self, query: str) -> dict:
        query_lower = query.lower()
        if "vacuum energy" in query_lower or "hypergraph expanding" in query_lower or "node generation" in query_lower:
            eval_res = self.evaluator.evaluate_hypergraph_rule("{x, y} -> {x, z}, {y, z}", 10)
            return {
                "agent": self.name,
                "query": query,
                "cag_type": "intrinsic_vacuum_energy_hypergraph",
                "result": eval_res
            }
        elif "oligon" in query_lower or "dark matter" in query_lower:
            units = self.unit_mgr.convert_oligon_mass_units(0.1) # 0.1 meV default
            density = self.data_tool.calculate_oligon_dark_matter_density(0.1, 1e20)
            return {
                "agent": self.name,
                "query": query,
                "cag_type": "oligon_dark_matter_mfdm",
                "units": units,
                "density": density
            }
        else:
            return {
                "agent": self.name,
                "query": query,
                "cag_type": "general_planck_cosmology",
                "params": self.data_tool.get_planck_cosmology_params()
            }

if __name__ == "__main__":
    agent = CosmologyAgent()
    print("Agent query test:", agent.route_query("Calculate vacuum energy of hypergraph expanding at N nodes"))
