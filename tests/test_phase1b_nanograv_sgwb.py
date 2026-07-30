"""
Unit and Integration Tests for Phase 1B NanoGrav SGWB Protocol
==============================================================
"""

import pytest
import numpy as np
import torch
from pathlib import Path

from hypergraph.oligon_simulations.gw_strain_extractor import GWStrainExtractor
from data_benchmarks.nanograv_loader import NANOGrav15yrLoader, fetch_nanograv_15yr_data
from scripts.nanograv_anisotropy import NANOGravAnisotropyMapper, map_nanograv_anisotropy
from scripts.bayesian_sgwb_verifier import BayesianSGWBVerifier, run_bayesian_model_selection


def test_compton_frequency_resonance():
    """Verify f_Compton equals 24.18 nHz for m_chi = 1e-22 eV."""
    extractor = GWStrainExtractor(m_chi_ev=1.0e-22)
    f_c = extractor.compute_compton_frequency()
    assert pytest.approx(f_c, abs=1e-10) == 2.418284e-8
    assert pytest.approx(f_c * 1e9, abs=0.1) == 24.18  # 24.18 nHz


def test_quadrupole_tensor_calculation():
    """Verify quadrupole tensor computation with 3D node positions."""
    extractor = GWStrainExtractor()
    adj = torch.eye(10, dtype=torch.float32)
    pos = torch.rand((10, 3), dtype=torch.float32)
    Q = extractor.compute_quadrupole_tensor(adj, pos)
    assert Q.shape == (3, 3)
    # Traceless check: sum of diagonal elements ~ 0
    trace = torch.trace(Q).item()
    assert abs(trace) < 1e-4


def test_characteristic_strain_extraction():
    """Verify characteristic strain computation and continuum slope."""
    extractor = GWStrainExtractor()
    Q_time = np.random.randn(50, 3, 3)
    freqs = np.linspace(1e-9, 1e-7, 14)
    res = extractor.compute_characteristic_strain(Q_time, dt=1.0, freqs=freqs)
    
    assert "h_c_total" in res
    assert "gamma_oligon" in res
    assert len(res["h_c_total"]) == 14
    assert res["f_compton_hz"] == extractor.f_compton


def test_nanograv_loader_real_data():
    """Verify loading real NANOGrav dataset products."""
    data = fetch_nanograv_15yr_data()
    assert "free_spectrum" in data
    assert "optimal_statistic" in data
    assert "pulsar_positions" in data
    assert data["num_pulsars"] >= 1


def test_anisotropy_mapping():
    """Verify C_l angular power spectrum calculation."""
    pulsar_positions = {
        f"J{i:02d}": {"ra_rad": 2.0 * np.pi * (i / 10.0), "dec_rad": np.arcsin(2.0 * (i / 10.0) - 1.0)}
        for i in range(10)
    }
    res = map_nanograv_anisotropy(pulsar_positions, max_l=4)
    assert "C_l_isotropic" in res
    assert "C_l_oligon_web" in res
    assert "anisotropy_ratio" in res
    assert res["max_multipole_l"] == 4


def test_bayesian_model_selection():
    """Verify Bayesian model selection, Bayes factor, and Delta BIC."""
    freqs = np.linspace(1e-9, 1e-7, 14)
    extractor = GWStrainExtractor()
    spec = extractor.compute_characteristic_strain(np.random.randn(50, 3, 3), dt=1.0, freqs=freqs)
    
    free_spec = {
        "frequencies_hz": freqs,
        "amplitude_matrix": np.tile(spec["h_c_total"], (50, 1))
    }
    
    verifier = BayesianSGWBVerifier()
    res = verifier.evaluate_bayesian_evidence(free_spec, spec)
    
    assert "delta_bic" in res
    assert "ln_bayes_factor_B10" in res
    assert "verdict" in res
    assert res["status"] == "SUCCESS"
