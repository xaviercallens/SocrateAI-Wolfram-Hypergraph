"""
Test Suite for Phase 3: N-Body Dynamics (Two-Body Oligon Attraction)
Validates that multi-way hypergraph rewrite rules A and B cause geodesic space contraction
between two K4 oligon tangles separated by a 20-edge vacuum cycle.
"""

from agents.topology_agent.topology_agent import TopologyAgent

def test_twobody_geodesic_attraction():
    agent = TopologyAgent(strict_cag_mode=True)
    res = agent.execute_twobody_attraction_poc(iterations=7)
    
    assert res["agent"] == "TopologyAgent"
    assert res["two_body_setup"]["initial_geodesic_distance"] == 10.0
    assert res["final_geodesic_distance"] < res["two_body_setup"]["initial_geodesic_distance"]
    assert res["delta_geodesic_distance"] < 0
    assert res["gravitational_attraction_proved"] is True
    assert res["lean4_verification"]["status"] == "verified"
    assert res["lean4_verification"]["theorem"] == "two_body_geodesic_attraction"
    
    print(f"Initial Geodesic Distance: {res['two_body_setup']['initial_geodesic_distance']}")
    print(f"Final Geodesic Distance at step 7: {res['final_geodesic_distance']}")
    print(f"Delta d (Gravitational Attraction): {res['delta_geodesic_distance']}")

if __name__ == "__main__":
    test_twobody_geodesic_attraction()
