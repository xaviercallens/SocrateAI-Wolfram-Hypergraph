import pytest
from mcp.tools.cosmology_data import CosmologyDataTool
from mcp.tools.evaluate_symbolic import SymbolicEvaluator
from mcp.tools.unit_manager import UnitManager


def test_cosmology_data():
    tool = CosmologyDataTool()
    params = tool.get_planck_cosmology_params()
    assert "H0_km_s_Mpc" in params

    res = tool.calculate_oligon_dark_matter_density(0.1, 1e20)
    assert res["oligon_mass_mev"] == 0.1
    assert res["defect_density_m3"] == 1e20


def test_evaluate_symbolic():
    evaluator = SymbolicEvaluator()
    res = evaluator.evaluate_hypergraph_rule("{x, y} -> {x, z}, {y, z}", 10)
    assert res["steps"] == 10


def test_unit_manager():
    um = UnitManager()
    with pytest.raises(ValueError):
        um.ev_to_log10_m_ev(-1.0)
    res = um.convert_oligon_mass_units(0.1)
    assert res["input_mass_mev"] == 0.1
