"""
Unit Test: GPU Accelerated Hypergraph Engine
Validates deep-time simulation performance on NVIDIA Tesla T4 GPU (CUDA).
"""

import pytest
import torch
from hypergraph.gpu_accelerated_engine import GPUHypergraphEngine


def test_gpu_accelerated_engine():
    engine = GPUHypergraphEngine()
    res = engine.run_gpu_deep_time_simulation(steps=20, initial_nodes=50)

    assert res["steps"] == 20
    assert res["initial_nodes"] == 50
    assert res["execution_time_sec"] < 5.0
    if torch.cuda.is_available():
        assert res["device"] == "cuda"
        assert "Tesla T4" in res["device_name"] or "NVIDIA" in res["device_name"]
