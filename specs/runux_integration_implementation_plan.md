# Implementation Plan: Runux AI Runtime Integration (v1.2)

**Target System:** `SocrateAI-Wolfram-Hypergraph` $\longleftrightarrow$ `Runux AI Runtime`  
**Specification Reference:** [runux_ai_runtime_integration_v1_1.md](file:///home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-GraphDarkMatter/SocrateAI-Wolfram-Hypergraph/specs/runux_ai_runtime_integration_v1_1.md)  
**Date:** July 28, 2026  
**Status:** Approved / Phase 0 MVP Active  

---

## Executive Summary & Phase 0 MVP Architecture

This implementation plan incorporates a low-cost, low-effort **Phase 0 (MVP): Single-Node Tensor Validation** on GCP Spot GPU hardware ($0.15/hr, < $100 budget). Phase 0 isolates and validates the core mathematical risk—PyTorch tensor masking $M_{t+1} = (M_t^2 + M_t) \odot T$ and in-memory Weisfeiler-Lehman canonical hashing—before proceeding to distributed multi-node architecture.

```
+-----------------------------------------------------------------------------------+
|                         PHASE 0 MVP (Single Spot GPU Node)                        |
|                                                                                   |
|  +-------------------------------------+      +--------------------------------+  |
|  |    phase0_tensor_masking.py         |      |    In-Memory RAM Ledger        |  |
|  |  - K4 Oligon + Vacuum Seed          |      |  - NetworkX Weisfeiler-Lehman   |  |
|  |  - PyTorch Hadamard Tensor Masking  | ---> |  - Permutation Invariant Hash  |  |
|  |    M_{t+1} = (M_t^2 + M_t) (o) T    |      |  - Python set() Branch Pruning |  |
|  +-------------------------------------+      +--------------------------------+  |
|                    |                                                              |
|                    v                                                              |
|  +-----------------------------------------------------------------------------+  |
|  | PASS GATE: VRAM < 15GB, Edge Count Bounded, 15 Iterations Complete          |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
                                     |
                                     v
+-----------------------------------------------------------------------------------+
|                     PHASES 1 - 4 (Distributed Production Scale)                   |
|                                                                                   |
|  Runux AI Runtime CUDA Kernels -> Redis Cluster Pruning -> GKE Multi-Pod -> CI/CD |
+-----------------------------------------------------------------------------------+
```

---

## Phase 0: Single-Node Tensor Validation MVP (Immediate Gate)

### Task 0.1: Develop Self-Contained MVP Script (`hypergraph/phase0_tensor_masking.py`)
- **Description:** Build a self-contained PyTorch script testing $M_{t+1} = (M_t^2 + M_t) \odot T$ on a $K_4$ Oligon + vacuum ring seed graph.
- **Target File:** `/hypergraph/phase0_tensor_masking.py`
- **Definition of Done (DoD):**
  - K4 defect seed and vacuum background ring initialized cleanly in PyTorch tensor format.
  - Topological mask $T$ flags defect interaction zones and preserves linear background edges.
  - Hadamard product execution stabilizes matrix sum and edge growth.
  - In-memory Weisfeiler-Lehman graph hashing (`nx.weisfeiler_lehman_graph_hash`) identifies isomorphic states.
- **Validation Criteria:**
  - Executed via `python3 hypergraph/phase0_tensor_masking.py`.
  - VRAM stays < 15 GB on Tesla T4; 15 iteration steps complete with zero OOM errors.
  - Edge count remains bounded at 36 edges; unmasked explosion ($641,620+$) is prevented.

### Task 0.2: Phase 0 Unit Test Suite (`tests/test_phase0_tensor_masking.py`)
- **Description:** Implement unit tests validating $K_4$ seed initialization, mask generation, canonical hashing invariance under node permutation, and full MVP simulation execution on CPU/GPU.
- **Target File:** `/tests/test_phase0_tensor_masking.py`
- **Definition of Done (DoD):**
  - Test verifies node permutations on $M_0$ produce identical Weisfeiler-Lehman hashes.
  - Test executes 5-step simulation and asserts success status.
- **Validation Criteria:**
  - `pytest tests/test_phase0_tensor_masking.py` passes 100%.

### Task 0.3: GCP Spot Provisioning Script (`deploy_gcp_phase0.sh`)
- **Description:** Provide automated `gcloud` provisioning script to deploy `hypergraph-mvp-t4` Spot Deep Learning VM on GCP.
- **Target File:** `/deploy_gcp_phase0.sh`
- **Definition of Done (DoD):**
  - Script specifies `n1-standard-4`, `SPOT` provisioning model, 1x NVIDIA Tesla T4 GPU, 50GB disk, and PyTorch image family.
- **Validation Criteria:**
  - `./deploy_gcp_phase0.sh` executes clean `gcloud` dry-run or creation command.

---

## Phase 1: Runux AI Runtime Core Integration (Aug 1 – Aug 29, 2026)

### Task 1.1: Develop `hypergraph/runux_engine.py` (Sparse Tensor Engine)
- **Description:** Implement a GPU-accelerated sparse matrix engine replacing legacy `gpu_accelerated_engine.py`. Utilize PyTorch sparse tensor representation (`torch.sparse_coo_tensor` or CSR format) and Runux CUDA kernels.
- **Target File:** `/hypergraph/runux_engine.py`
- **Definition of Done (DoD):**
  - Engine accepts adjacency tensors in CSR/COO format.
  - Multi-way step evolution uses optimized sparse matmul ($M_t^2 + M_t$).
- **Validation Criteria:**
  - `pytest tests/test_runux_engine.py` passes on matrices up to $10,000 \times 10,000$.

### Task 1.2: Develop `hypergraph/tensor_masking.py` (Topological Masking $T$)
- **Description:** Implement topological mask tensors $T$ and Hadamard multiplication logic ($M_{t+1} = (M_t^2 + M_t) \odot T$) to restrict rewrite expansions to valid $K_4$ defect zones.
- **Target File:** `/hypergraph/tensor_masking.py`
- **Definition of Done (DoD):**
  - Implement `apply_topological_mask()` returning elementwise Hadamard product.
  - Implement `topological_relu` to prune non-physical noise edges.
- **Validation Criteria:**
  - `pytest tests/test_topological_masking.py` verifies edge count saturation is prevented.

---

## Phase 2: Distributed Isomorphic Pruning (Aug 29 – Sep 19, 2026)

### Task 2.1: Implement Canonical Graph Labeling & Hashing (`hypergraph/canonical_ledger.py`)
- **Target File:** `/hypergraph/canonical_ledger.py`
- **Definition of Done (DoD):**
  - Implement Nauty/Bliss canonical reordering (`get_canonical_label`) and SHA-256 state hashing.
- **Validation Criteria:**
  - `pytest tests/test_canonical_hashing.py` passes with 100 permuted isomorphic graph pairs.

### Task 2.2: Deploy Distributed Redis Ledger Integration
- **Target File:** `/hypergraph/canonical_ledger.py`
- **Definition of Done (DoD):**
  - Query and record state SHA-256 hashes against GKE Redis cluster with < 1ms latency.
- **Validation Criteria:**
  - `pytest tests/test_redis_pruning.py` confirms duplicate states are pruned. Compression target > 95%.

---

## Phase 3: Real-World Data Benchmarking (Sep 19 – Oct 17, 2026)

### Task 3.1: Develop Empirical Cosmological Data Loader (`data_benchmarks/sdss_validator.py`)
- **Target Files:** `/data_benchmarks/sdss_validator.py`, `/data_benchmarks/planck_validator.py`
- **Validation Criteria:**
  - `pytest tests/test_cosmology_data_loaders.py` validates empirical power spectrum calculations.

### Task 3.2: Extract Large-$N$ Thermodynamic Continuum Limit
- **Target File:** `/hypergraph/continuum_limits/thermodynamic_limit.py`
- **Validation Criteria:**
  - `pytest tests/test_thermodynamic_limit.py` verifies spatial power spectrum $P_{\text{sim}}(k)$ as $N \to \infty$.

---

## Phase 4: Infrastructure, Monitoring, & CI/CD (Oct 17 – Oct 31, 2026)

### Task 4.1: Containerization & GKE Manifests
- **Target Files:** `Dockerfile`, `/k8s/runux-deployment.yaml`, `/k8s/redis-cluster.yaml`
- **Validation Criteria:**
  - `docker build` succeeds and `kubectl apply --dry-run=client` validates clean manifests.

---

## Summary Matrix of Deliverables & Test Targets

| Phase | Core Deliverable File | Target Test File | Success Metric / Gate |
|---|---|---|---|
| **Phase 0 MVP** | `/hypergraph/phase0_tensor_masking.py`<br>`deploy_gcp_phase0.sh` | `tests/test_phase0_tensor_masking.py` | VRAM < 15GB on T4;<br>36 edges bounded (Masked sum = 1,610 vs Unmasked = 641,620+);<br>GCP burn rate ~$0.15/hr (< $100 budget). |
| **Phase 1** | `/hypergraph/runux_engine.py`<br>`/hypergraph/tensor_masking.py` | `tests/test_topological_masking.py`<br>`tests/test_runux_engine.py` | Ops/sec > 10,000 on T4;<br>Zero exponential edge explosion. |
| **Phase 2** | `/hypergraph/canonical_ledger.py` | `tests/test_canonical_hashing.py`<br>`tests/test_redis_pruning.py` | Isomorphic hash identity = 100%;<br>Pruning compression > 95%. |
| **Phase 3** | `/data_benchmarks/sdss_validator.py` | `tests/test_empirical_benchmark.py` | Automated $\chi^2$ comparison vs SDSS/Planck data. |
| **Phase 4** | `/k8s/runux-deployment.yaml`<br>`.github/workflows/runux-ci.yml` | `tests/test_monitoring.py` | Docker build green;<br>GKE manifest dry-run clean. |
