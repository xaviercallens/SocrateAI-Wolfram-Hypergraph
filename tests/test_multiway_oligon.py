"""
Unit Test: Multi-Way Evolution & Oligon Tangle Defect Simulation
Validates Phase 1 (Causal Variance & Branching) and Phase 2 (Oligon MFDM Localized Curvature).
"""

from hypergraph.rewrite_rules.multiway_rules import MultiWayRule
from hypergraph.oligon_simulations.oligon_defect_sim import OligonDefectSimulator

def test_multiway_causal_branching():
    mw = MultiWayRule("Test_MultiWay", [("{x,y}", "{x,z},{y,z}")])
    initial_edges = [(1, 2), (2, 3), (3, 1)]
    res = mw.generate_multiway_step(initial_edges)
    
    assert res["num_branches"] >= 3
    assert res["causal_variance_measure"] > 0
    assert any(b["rule_applied"] == "oligon_defect_spawn" for b in res["branches"])

def test_oligon_tangle_defect_simulation():
    sim = OligonDefectSimulator(core_nodes=4, background_nodes=10)
    res = sim.simulate_density_evolution(steps=10)
    
    assert res["final_edges"] > res["initial_edges"]
    assert res["final_core_density_ratio"] > 0
    assert "rho_0_central_density" in res["mfdm_soliton_profile_fit"]
    assert "solitonProfile" in res["wolfram_script"]
