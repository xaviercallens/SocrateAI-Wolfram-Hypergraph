# MEMORY.md — SocrateAI Wolfram Hypergraph Session State & Recovery

**Last Updated:** 2026-07-28  
**Repository:** `SocrateAI-Wolfram-Hypergraph`  
**Status:** ✅ Fully Operational — 19/19 Tests Passing  

---

## 1. Quick Verification & Test Run

To verify code integrity at any time:
```bash
cd /home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-GraphDarkMatter/SocrateAI-Wolfram-Hypergraph
PYTHONPATH=. pytest --cov=hypergraph tests/
```

Expected Output:
- `19 passed in ~3.4s`
- Coverage: ~90% on core hypergraph modules.

---

## 2. Directory & Module Roadmap

- `hypergraph/`
  - `rewrite_rules/`: Core rule abstractions (`rules.py`, `multiway_rules.py`).
  - `gpu_accelerated_engine.py`: PyTorch tensor-based hypergraph state evolution.
  - `oligon_simulations/`: Oligon topological defect simulations (`oligon_defect_sim.py`, `oligon_mfdm_mapper.py`).
  - `continuum_limits/`: Continuum vacuum energy and dark matter calculations (`vacuum_energy_calculator.py`).
- `agents/`
  - `core_base_agent.py`: Base agent structure with LLM tool invocation.
  - `cosmology_agent/`: Cosmological calculation agent.
  - `topology_agent/`: Hypergraph rewriting and K3 topological defect agent.
- `mcp/`
  - `tools/`: Model Context Protocol tools (`cosmology_data.py`, `hypergraph_rewriter.py`).
- `specs/`
  - `system_specification.md`: Comprehensive system architecture and data structures.
  - `runux_integration_architecture.md`: Architecture for PyTorch Sparse Tensor Hadamard masking ($M_{t+1} = (M_t^2 + M_t) \odot T$).
- `tests/`: Full pytest test suite.

---

## 3. Key Recovery Information

- **Root Memory Link:** [Root MEMORY.md](file:///home/callensxavier_gmail_com/MEMORY.md)
- **Start Here Guide:** [START_HERE.md](file:///home/callensxavier_gmail_com/START_HERE.md)
- **System Spec:** [system_specification.md](file:///home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-GraphDarkMatter/SocrateAI-Wolfram-Hypergraph/specs/system_specification.md)
- **Runux Architecture Spec:** [runux_integration_architecture.md](file:///home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-GraphDarkMatter/SocrateAI-Wolfram-Hypergraph/specs/runux_integration_architecture.md)

---

## 4. Current Status & Next Milestones

1. **State Persistence & Recovery:** `MEMORY.md` created at root and repository level.
2. **Phase 3 Scaled Runtime Prototype:** Implementing PyTorch Sparse Tensor Hadamard masking prototype with `topological_relu` in `hypergraph/runux_tensor_mask.py`.
3. **Integration with Runux C++ Engine:** Linking sparse matrix output from PyTorch engine to Runux C++ backend.
