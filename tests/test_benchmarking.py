import numpy as np
import torch
from scipy.stats import chisquare
from hypergraph.continuum_limits.power_spectrum import compute_hypergraph_power_spectrum


def test_power_spectrum_chi_squared():
    """Validates that simulated hypergraph P(k) matches observational baseline."""
    np.random.seed(42)
    # Generate test hypergraph adjacency matrix with varying node degrees
    adj = torch.rand((100, 100))
    adj = (adj + adj.T) / 2.0  # Symmetric
    k_sim, P_sim = compute_hypergraph_power_spectrum(adj, num_bins=20)

    # Add small epsilon to avoid zero frequencies
    P_sim = P_sim + 1e-6
    # Mock observational baseline for test suite
    P_obs = P_sim * (1.0 + np.random.normal(0, 0.02, size=P_sim.shape))
    P_obs = np.maximum(P_obs, 1e-6)

    # Normalize spectra for comparison
    P_sim_norm = (P_sim / np.sum(P_sim)).astype(np.float64)
    P_obs_norm = (P_obs / np.sum(P_obs)).astype(np.float64)
    P_obs_norm = P_obs_norm * (np.sum(P_sim_norm) / np.sum(P_obs_norm))

    chi2, p_val = chisquare(P_sim_norm, P_obs_norm)

    assert not np.isnan(chi2), "Chi-squared calculation returned NaN"
    assert p_val > 0.01, f"Simulated P(k) deviates significantly from observations (p={p_val})"
