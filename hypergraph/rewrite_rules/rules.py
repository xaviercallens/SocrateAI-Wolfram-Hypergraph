"""
Hypergraph Rewrite Rules Definition
Defines deterministic spatial updating rules for hypergraph evolution.
"""

from typing import Dict, Any, List

class RewriteRule:
    """Represents a hypergraph substitution rule."""

    def __init__(self, name: str, pattern: str, substitution: str, growth_factor: float):
        self.name = name
        self.pattern = pattern
        self.substitution = substitution
        self.growth_factor = growth_factor

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "pattern": self.pattern,
            "substitution": self.substitution,
            "growth_factor": self.growth_factor
        }

# Core Stream 4 Rules
RULE_BINARY_SPLIT = RewriteRule(
    name="Binary Edge Division",
    pattern="{x, y}",
    substitution="{x, z}, {y, z}",
    growth_factor=2.0
)

RULE_TERNARY_EXPANSION = RewriteRule(
    name="Ternary Hyperedge Division",
    pattern="{x, y, z}",
    substitution="{x, w, z}, {y, w, z}",
    growth_factor=2.0
)
