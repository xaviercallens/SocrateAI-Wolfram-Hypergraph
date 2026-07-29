import torch
import pytest
from hypergraph.topology_metrics import extract_spectral_gap


def test_extract_spectral_gap_dod():
    # Construct a diagonal matrix with eigenvalues [400.0, 1.0, 0.5, 0.1]
    evals = torch.tensor([400.0, 1.0, 0.5, 0.1])
    matrix = torch.diag(evals)

    metrics = extract_spectral_gap(matrix, k=4)
    assert metrics["lambda_1"] == pytest.approx(400.0)
    assert metrics["lambda_2"] == pytest.approx(1.0)
    assert metrics["spectral_gap"] == pytest.approx(399.0)


def test_extract_spectral_gap_sparse():
    evals = torch.tensor([10.0, 5.0, 2.0])
    dense_matrix = torch.diag(evals)
    sparse_matrix = dense_matrix.to_sparse()

    metrics = extract_spectral_gap(sparse_matrix, k=3)
    assert metrics["spectral_gap"] == pytest.approx(5.0)
