"""
Test Suite for Simultaneous K3 vs K4 vs K5 Mass Spectrum Trial (Isomorphic Pruned)
Validates state-space pruning, sub-threshold K3 evaporation, K4 minimal soliton boundary,
and K5 deep gravity well formation.
"""

from agents.topology_agent.topology_agent import TopologyAgent

def test_k3_k4_k5_pruned_spectrum_trial():
    agent = TopologyAgent(strict_cag_mode=True)
    res = agent.execute_k3_k4_k5_mass_spectrum_trial_pruned(iterations=10, pruning_mode="aggressive")
    
    assert res["agent"] == "TopologyAgent"
    assert res["simulation_type"] == "K3 vs K4 vs K5 Mass Spectrum Trial (Isomorphic Pruned)"
    assert res["hardware_accelerator"]["isomorphism_pruning"] == "aggressive"
    
    spec = res["spectrum_results"]
    
    # K3 Evaporation
    assert spec["K3_triangle"]["final_integrity"] == 0.0
    assert spec["K3_triangle"]["evaporated"] is True
    
    # K4 Stable Soliton Threshold
    assert spec["K4_tetrahedron"]["final_integrity"] > 6.0
    assert spec["K4_tetrahedron"]["soliton_stable"] is True
    
    # K5 Deep Gravity Well
    assert spec["K5_pentagram"]["final_integrity"] > spec["K4_tetrahedron"]["final_integrity"]
    assert spec["K5_pentagram"]["curvature_ratio_R"] > 1.0
    
    # Conclusions & Verification
    assert res["lean4_verification"]["status"] == "verified"
    assert res["lean4_verification"]["theorem"] == "k3_evaporates_k4_stable_k5_gravity_well"
    
    print(f"Pruning Efficiency: {res['hardware_accelerator']['pruning_efficiency_ratio']}")
    print(f"K3 Integrity: {spec['K3_triangle']['final_integrity']} (Evaporated)")
    print(f"K4 Integrity: {spec['K4_tetrahedron']['final_integrity']} (Stable Soliton)")
    print(f"K5 Integrity: {spec['K5_pentagram']['final_integrity']} (Deep Gravity Well R={spec['K5_pentagram']['curvature_ratio_R']})")

if __name__ == "__main__":
    test_k3_k4_k5_pruned_spectrum_trial()
