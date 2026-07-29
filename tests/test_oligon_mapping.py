"""
Unit Test: Oligon Topological Defect to MFDM Mapping
Verifies that Oligon tangle defects in hypergraphs map deterministically to Fuzzy Dark Matter wave parameters.
"""

import pytest
from hypergraph.oligon_simulations.oligon_mfdm_mapper import OligonMFDMMapper
from mcp.tools.unit_manager import UnitManager


def test_oligon_mapping():
    mapper = OligonMFDMMapper(oligon_winding_number=1, core_mass_mev=0.1)
    res = mapper.calculate_continuum_wavefunction_params()

    assert res["oligon_winding_number"] == 1
    assert res["oligon_mass_mev"] == 0.1
    assert res["oligon_mass_ev"] == 0.0001
    assert res["soliton_core_radius_kpc"] > 0
    assert res["mfdm_continuum_match"] == "VERIFIED"


def test_unit_manager_conversion():
    res = UnitManager.convert_oligon_mass_units(0.1)
    assert res["input_mass_mev"] == 0.1
    assert res["mass_ev"] == 0.0001
    assert pytest.approx(res["log10_m_ev"], 0.01) == -4.0
    assert res["dimensional_check"] == "PASSED"
