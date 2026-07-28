import pytest
from hypergraph.rewrite_rules.rules import RewriteRule, RULE_BINARY_SPLIT, RULE_TERNARY_EXPANSION

def test_rewrite_rule():
    rule = RewriteRule("test", "{a}", "{b}", 1.5)
    d = rule.to_dict()
    assert d["name"] == "test"
    assert d["pattern"] == "{a}"
    assert d["substitution"] == "{b}"
    assert d["growth_factor"] == 1.5

def test_constants():
    d1 = RULE_BINARY_SPLIT.to_dict()
    assert d1["name"] == "Binary Edge Division"
    
    d2 = RULE_TERNARY_EXPANSION.to_dict()
    assert d2["name"] == "Ternary Hyperedge Division"
