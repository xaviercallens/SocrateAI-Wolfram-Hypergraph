import pytest
from agents.core.base_agent import BaseCAGAgent

def test_base_agent():
    agent = BaseCAGAgent(name="TestAgent")
    assert agent.strict_cag_mode is True
    prompt = agent.format_cag_system_prompt()
    assert "TestAgent" in prompt
    
    with pytest.raises(NotImplementedError):
        agent.route_query("test")
