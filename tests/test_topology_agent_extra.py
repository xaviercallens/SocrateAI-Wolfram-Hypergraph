import pytest
from agents.topology_agent.topology_agent import TopologyAgent


def test_topology_agent_extra_coverage():
    agent = TopologyAgent()
    res = agent.execute_multiway_oligon_poc(2)
    assert res["emergent_gravity_result"] in [
        "EMERGENT_GRAVITY_DEMONSTRATED (R > 1.0)", "FLAT_VACUUM"]
