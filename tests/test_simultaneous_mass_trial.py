"""
Test Suite for Simultaneous K3 vs K5 Mass Spectrum Trial
Validates simultaneous evaporation of sub-threshold K3 triangle defect
and formation of deep topological gravity well by super-critical K5 pentagram defect.
"""

from agents.topology_agent.topology_agent import TopologyAgent

def test_simultaneous_k3_k5_trial():
    agent = TopologyAgent(strict_cag_mode=True)
    res = agent.execute_simultaneous_k3_k5_spectrum_trial(iterations=10)
    
    assert res["agent"] == "TopologyAgent"
    assert res["simulation_type"] == "Simultaneous K3 vs K5 Mass Spectrum Trial"
    
    # K3 assertions
    k3_res = res["k3_triangle_tangle"]
    assert k3_res["final_integrity"] == 0.0
    assert k3_res["evaporated"] is True
    assert k3_res["physical_state"] == "EVAPORATED_INTO_VACUUM_DISPERSION"
    
    # K5 assertions
    k5_res = res["k5_pentagram_tangle"]
    assert k5_res["final_integrity"] > k5_res["initial_edges"]
    assert k5_res["curvature_ratio_R"] > 1.0
    assert k5_res["physical_state"] == "DEEP_TOPOLOGICAL_GRAVITY_WELL"
    
    # Conclusions
    assert res["trial_conclusions"]["k3_evaporation_confirmed"] is True
    assert res["trial_conclusions"]["k5_deep_well_confirmed"] is True
    assert res["lean4_verification"]["status"] == "verified"
    assert res["lean4_verification"]["theorem"] == "k3_evaporates_and_k5_forms_gravity_well"
    
    print(f"K3 Final Integrity: {k3_res['final_integrity']} (Evaporated)")
    print(f"K5 Final Integrity: {k5_res['final_integrity']} (Curvature R = {k5_res['curvature_ratio_R']})")

if __name__ == "__main__":
    test_simultaneous_k3_k5_trial()
