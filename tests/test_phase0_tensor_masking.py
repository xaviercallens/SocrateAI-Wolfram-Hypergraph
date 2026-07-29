"""
Unit test for Phase 0 MVP: Single-Node Tensor Validation
"""

import pytest
import torch
from hypergraph.phase0_tensor_masking import (
    create_k4_oligon_seed,
    generate_topological_mask,
    canonical_graph_hash,
    run_phase0_simulation
)


def test_k4_oligon_seed_creation():
    M_0 = create_k4_oligon_seed(vacuum_size=6)
    assert M_0.shape == (10, 10)
    # Check K4 sub-block is complete (off-diagonal entries = 1.0)
    assert M_0[0, 1] == 1.0
    assert M_0[1, 2] == 1.0
    assert M_0[2, 3] == 1.0


def test_topological_mask_generation():
    M_0 = create_k4_oligon_seed(vacuum_size=6)
    T = generate_topological_mask(M_0)
    assert T.shape == M_0.shape
    assert (T >= 0.0).all() and (T <= 1.0).all()


def test_canonical_graph_hash():
    M_0 = create_k4_oligon_seed(vacuum_size=6)
    hash_1 = canonical_graph_hash(M_0)

    # Permute node order (nodes 0 and 1 swapped)
    perm = list(range(10))
    perm[0], perm[1] = 1, 0
    M_permuted = M_0[perm][:, perm]

    hash_2 = canonical_graph_hash(M_permuted)
    # Isomorphic graphs must yield identical hash
    assert hash_1 == hash_2


def test_run_phase0_simulation():
    res = run_phase0_simulation(max_steps=5, device="cpu")
    assert res["status"] == "SUCCESS"
    assert res["max_steps"] == 5
    assert res["unique_hashes"] > 0
    assert len(res["history"]) == 5
