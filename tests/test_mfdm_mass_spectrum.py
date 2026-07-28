"""
Test Suite for Option B: MFDM Mass Spectrum Trial (Finding the Limits)
Validates topological seeds (K3, K4, K5) against background Rule A vacuum expansion rate.
"""

from agents.topology_agent.topology_agent import TopologyAgent

def test_mfdm_mass_spectrum_limits():
    agent = TopologyAgent(strict_cag_mode=True)
    res = agent.execute_mfdm_mass_spectrum_trial(iterations=10)
    
    assert res["agent"] == "TopologyAgent"
    assert res["simulation_type"] == "MFDM Mass Spectrum Trial (Topological Limits)"
    
    # Assert K3 dissolution
    k3_res = res["topological_seeds_tested"]["K3"]
    assert k3_res["status"] == "DISSOLVED_BY_DARK_ENERGY"
    assert k3_res["mfdm_mass_state"] == "SUB_THRESHOLD_DISPERSION"
    
    # Assert K4 stability (Minimal Stable Seed)
    k4_res = res["topological_seeds_tested"]["K4"]
    assert k4_res["status"] == "BOUND_SOLITON_PRESERVED"
    assert k4_res["mfdm_mass_state"] == "THRESHOLD_STABLE_SOLITON"
    
    # Assert K5 ultra-dense core
    k5_res = res["topological_seeds_tested"]["K5"]
    assert k5_res["status"] == "BOUND_SOLITON_PRESERVED"
    assert k5_res["mfdm_mass_state"] == "ULTRA_DENSE_CORE"
    
    # Verification assertions
    assert res["mfdm_threshold_conclusion"]["minimal_stable_seed"] == "K4 (Tetrahedron complete graph)"
    assert res["lean4_verification"]["status"] == "verified"
    assert res["lean4_verification"]["theorem"] == "k3_dissolves_under_expansion"
    
    print("K3 Status:", k3_res["status"])
    print("K4 Status:", k4_res["status"])
    print("K5 Status:", k5_res["status"])

if __name__ == "__main__":
    test_mfdm_mass_spectrum_limits()
