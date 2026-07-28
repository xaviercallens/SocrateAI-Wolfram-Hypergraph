import pytest
from agents.cosmology_agent.cosmology_agent import CosmologyAgent

def test_cosmology_agent_routing():
    agent = CosmologyAgent()
    
    # Test Vacuum Energy routing
    res1 = agent.route_query("calculate vacuum energy")
    assert res1["cag_type"] == "intrinsic_vacuum_energy_hypergraph"
    
    # Test Oligon routing
    res2 = agent.route_query("calculate oligon properties")
    assert res2["cag_type"] == "oligon_dark_matter_mfdm"
    assert "units" in res2
    assert "density" in res2
    
    # Test general routing
    res3 = agent.route_query("what is the hubble constant?")
    assert res3["cag_type"] == "general_planck_cosmology"
    assert "params" in res3

