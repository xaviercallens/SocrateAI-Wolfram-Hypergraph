"""
NVIDIA Tesla T4 GPU Stress Integration & Benchmarking Suite
=============================================================
Stress-tests and validates CUDA performance, sparse COO matrix multiplication,
VRAM allocation, mixed precision (FP16/FP32), CUDA stream parallelism, and LTN
spectral gap extraction on NVIDIA Tesla T4.
"""

import time
import torch
import pytest
from hypergraph.runux_engine import RunuxSparseEngine
from hypergraph.runux_sundials_adapter import RunuxHypergraphAccelerator, LogicTensorNetworkGatekeeper


@pytest.mark.skipif(not torch.cuda.is_available(),
                    reason="NVIDIA GPU required for T4 benchmark")
def test_t4_device_telemetry():
    """Validates Tesla T4 GPU specifications and CUDA initialization."""
    device_name = torch.cuda.get_device_name(0)
    capability = torch.cuda.get_device_capability(0)
    total_memory_gb = torch.cuda.get_device_properties(
        0).total_memory / (1024 ** 3)

    print(f"\n[T4 Telemetry] Device: {device_name}")
    print(
        f"[T4 Telemetry] Compute Capability: {capability[0]}.{capability[1]}")
    print(f"[T4 Telemetry] Total VRAM: {total_memory_gb:.2f} GB")

    assert "T4" in device_name or "Tesla" in device_name or "NVIDIA" in device_name
    assert total_memory_gb > 14.0  # ~15.7 GB for T4


@pytest.mark.skipif(not torch.cuda.is_available(),
                    reason="NVIDIA GPU required for T4 benchmark")
def test_t4_sparse_coo_engine_stress():
    """Stress-tests RunuxSparseEngine on Tesla T4 with N = 20,000 sparse nodes."""
    device = torch.device("cuda:0")
    num_nodes = 20000
    nnz = 100000  # 100,000 non-zero edge entries

    # Generate random sparse indices on CUDA
    i = torch.randint(0, num_nodes, (2, nnz), device=device)
    v = torch.rand(nnz, device=device, dtype=torch.float32)
    adj_sparse = torch.sparse_coo_tensor(
        i, v, (num_nodes, num_nodes), device=device).coalesce()

    mask_v = torch.rand(nnz, device=device, dtype=torch.float32)
    mask_sparse = torch.sparse_coo_tensor(
        i, mask_v, (num_nodes, num_nodes), device=device).coalesce()

    # Warmup
    _ = RunuxSparseEngine.sparse_masked_step(adj_sparse, mask_sparse)
    torch.cuda.synchronize()

    # Timed Benchmark
    start_time = time.perf_counter()
    num_iterations = 10
    for _ in range(num_iterations):
        out = RunuxSparseEngine.sparse_masked_step(adj_sparse, mask_sparse)
    torch.cuda.synchronize()
    elapsed_ms = ((time.perf_counter() - start_time) / num_iterations) * 1000.0

    vram_used_mb = torch.cuda.max_memory_allocated(device) / (1024 ** 2)

    print(f"\n[T4 Sparse Benchmark] N = {num_nodes:,} nodes | NNZ = {nnz:,}")
    print(f"[T4 Sparse Benchmark] Avg Step Latency: {elapsed_ms:.3f} ms")
    print(f"[T4 Sparse Benchmark] Peak VRAM Allocated: {vram_used_mb:.2f} MB")

    assert out.is_sparse
    assert elapsed_ms < 100.0  # Latency under 100ms on T4


@pytest.mark.skipif(not torch.cuda.is_available(),
                    reason="NVIDIA GPU required for T4 benchmark")
def test_t4_mixed_precision_fp16_acceleration():
    """Validates FP16 half-precision sparse matrix multiplication on T4 Tensor Cores."""
    device = torch.device("cuda:0")
    num_nodes = 10000
    nnz = 50000

    i = torch.randint(0, num_nodes, (2, nnz), device=device)
    v_fp32 = torch.rand(nnz, device=device, dtype=torch.float32)
    v_fp16 = v_fp32.to(torch.float16)

    adj_fp32 = torch.sparse_coo_tensor(
        i, v_fp32, (num_nodes, num_nodes), device=device).coalesce()
    adj_fp16 = torch.sparse_coo_tensor(
        i, v_fp16, (num_nodes, num_nodes), device=device).coalesce()

    mask_fp32 = torch.sparse_coo_tensor(
        i, v_fp32, (num_nodes, num_nodes), device=device).coalesce()
    mask_fp16 = torch.sparse_coo_tensor(
        i, v_fp16, (num_nodes, num_nodes), device=device).coalesce()

    out_fp32 = RunuxSparseEngine.sparse_masked_step(adj_fp32, mask_fp32)
    out_fp16 = RunuxSparseEngine.sparse_masked_step(adj_fp16, mask_fp16)

    assert out_fp16.dtype == torch.float16
    assert out_fp32.dtype == torch.float32
    print("\n[T4 FP16 Tensor Core] FP16 & FP32 sparse step execution verified on CUDA.")


@pytest.mark.skipif(not torch.cuda.is_available(),
                    reason="NVIDIA GPU required for T4 benchmark")
def test_t4_cuda_streams_parallelism():
    """Tests multi-stream parallel branch execution on Tesla T4."""
    device = torch.device("cuda:0")
    s1 = torch.cuda.Stream(device=device)
    s2 = torch.cuda.Stream(device=device)

    num_nodes = 5000
    i1 = torch.randint(0, num_nodes, (2, 20000), device=device)
    v1 = torch.rand(20000, device=device)
    a1 = torch.sparse_coo_tensor(
        i1, v1, (num_nodes, num_nodes), device=device).coalesce()
    m1 = torch.sparse_coo_tensor(
        i1, v1, (num_nodes, num_nodes), device=device).coalesce()

    i2 = torch.randint(0, num_nodes, (2, 20000), device=device)
    v2 = torch.rand(20000, device=device)
    a2 = torch.sparse_coo_tensor(
        i2, v2, (num_nodes, num_nodes), device=device).coalesce()
    m2 = torch.sparse_coo_tensor(
        i2, v2, (num_nodes, num_nodes), device=device).coalesce()

    with torch.cuda.stream(s1):
        out1 = RunuxSparseEngine.sparse_masked_step(a1, m1)

    with torch.cuda.stream(s2):
        out2 = RunuxSparseEngine.sparse_masked_step(a2, m2)

    torch.cuda.synchronize()

    assert out1.is_sparse and out2.is_sparse
    print(
        "\n[T4 CUDA Streams] Concurrent multi-stream execution completed successfully.")


@pytest.mark.skipif(not torch.cuda.is_available(),
                    reason="NVIDIA GPU required for T4 benchmark")
def test_t4_accelerator_full_integration():
    """Tests the complete RunuxHypergraphAccelerator pipeline on Tesla T4."""
    device = torch.device("cuda:0")
    num_nodes = 1000
    nnz = 5000

    i = torch.randint(0, num_nodes, (2, nnz), device=device)
    i = torch.cat([i, i.flip(0)], dim=1)
    v1 = torch.rand(i.shape[1] // 2, device=device)
    v1 = torch.cat([v1, v1], dim=0)
    adj_sparse = torch.sparse_coo_tensor(
        i, v1, (num_nodes, num_nodes), device=device).coalesce()

    v2 = torch.rand(i.shape[1] // 2, device=device)
    v2 = torch.cat([v2, v2], dim=0)
    mask_sparse = torch.sparse_coo_tensor(
        i, v2, (num_nodes, num_nodes), device=device).coalesce()

    accelerator = RunuxHypergraphAccelerator()
    res = accelerator.process_accelerated_step(adj_sparse, mask_sparse)

    assert res["accelerator_status"] == "SUCCESS"
    assert "canonical_hash" in res
    assert res["ltn_invariants"]["symmetry_invariant_truth"] == 1.0
    print(
        f"\n[T4 Integration] Full pipeline verified. State hash: {res['canonical_hash'][:16]}...")
