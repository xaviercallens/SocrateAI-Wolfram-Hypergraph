import re

with open('agents/topology_agent/topology_agent.py', 'r') as f:
    content = f.read()

# Add imports
content = content.replace('from typing import Dict, Any', 'from typing import Dict, Any\nfrom mcp.tools.evaluate_symbolic import SymbolicEvaluator\nfrom mcp.tools.lean_verifier import Lean4Verifier')

# Add to __init__
init_replace = """        self.enable_multiway_graphs = enable_multiway_graphs
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.evaluator = SymbolicEvaluator()
        self.lean_verifier = Lean4Verifier()"""
content = content.replace('        self.enable_multiway_graphs = enable_multiway_graphs\n        self.device = "cuda" if torch.cuda.is_available() else "cpu"', init_replace)

# write it back
with open('agents/topology_agent/topology_agent.py', 'w') as f:
    f.write(content)
