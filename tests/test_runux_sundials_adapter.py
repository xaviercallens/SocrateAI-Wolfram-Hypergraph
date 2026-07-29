import torch
import pytest
from hypergraph.runux_sundials_adapter import (
    LogicTensorNetworkGatekeeper,
    RustySundialsDualAutoDiffSolver,
    RunuxHypergraphAccelerator,
)


def test_logic_tensor_network_gatekeeper():
    evals = torch.tensor([400.0, 1.0, 0.5, 0.1])
    matrix = torch.diag(evals)

    gatekeeper = LogicTensorNetworkGatekeeper(target_spectral_gap=399.0)
    eval_res = gatekeeper.evaluate_predicates(matrix)

    assert eval_res["spectral_gap_invariant_truth"] == pytest.approx(1.0)
    assert eval_res["symmetry_invariant_truth"] == 1.0
    assert eval_res["overall_ltn_truth_value"] == 1.0
    assert eval_res["lean4_certification_status"] == "VERIFIED_CERT_LEAN4_AUTO"


def test_rusty_sundials_dual_autodiff_solver():
    matrix = torch.eye(4)
    solver = RustySundialsDualAutoDiffSolver()
    updated = solver.step_dual_forward(matrix, dt=0.01)

    assert updated.shape == (4, 4)
    # M_t=I -> M_t^2 + M_t = 2I -> step: I + 0.01*(2I) = 1.02 I
    expected = torch.eye(4) * 1.02
    assert torch.allclose(updated, expected)


def test_runux_hypergraph_accelerator():
    adj_sparse = torch.eye(4).to_sparse().coalesce()
    mask_sparse = torch.ones((4, 4)).to_sparse().coalesce()

    accelerator = RunuxHypergraphAccelerator()
    res = accelerator.process_accelerated_step(adj_sparse, mask_sparse)

    assert res["accelerator_status"] == "SUCCESS"
    assert "canonical_hash" in res
    assert res["ltn_invariants"]["overall_ltn_truth_value"] >= 0.0
