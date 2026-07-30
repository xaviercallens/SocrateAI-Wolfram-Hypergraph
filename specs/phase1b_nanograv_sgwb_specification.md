# Phase 1B Experimental Specification & Implementation Plan
## NanoGrav Stochastic Gravitational Wave Background (SGWB) $K_4$ Oligon Fingerprint & Bayesian Model Selection

**Document Version:** 1.0 (Specification & Architecture Draft)  
**Date:** July 30, 2026  
**Author:** HyperGraphAstro Pipeline Lead  
**Repository:** `xaviercallens/SocrateAI-Wolfram-Hypergraph`  
**Target Specs Location:** [specs/phase1b_nanograv_sgwb_specification.md](file:///home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-GraphDarkMatter/SocrateAI-Wolfram-Hypergraph/specs/phase1b_nanograv_sgwb_specification.md)  
**Status:** 🎯 Approved Specification — Pending Execution

---

## Executive Summary

The **Phase 1B Experiment** provides a definitive, falsifiable test comparing the **Dual-Scale $K_4$ Oligon Hypergraph Cosmology** against the standard Supermassive Black Hole Binary (SMBHB) merger model for the Stochastic Gravitational Wave Background (SGWB) recently detected by the **NANOGrav 15-Year Dataset**.

By isolating the **Compton Frequency Resonance** of ultra-light Mixed-Fraction Fuzzy Dark Matter (MFDM) halos ($m_\chi \approx 10^{-22}\text{ eV}$) at $f \approx 2.4 \times 10^{-8}\text{ Hz}$ (24 nHz) and extracting the exact spectral index $\gamma_{\text{oligon}}$ and angular anisotropy $C_\ell$ from discrete hypergraph $K_4$ merger checkpoints, Phase 1B will execute rigorous Bayesian model selection against live NANOGrav pulsar timing array residuals.

---

## 1. Theoretical Physics: The Compton Frequency Resonance

### 1.1 Physical Mechanism
In the Dual-Scale Hypergraph Cosmology, $K_4$ complete subgraphs act as topological defect tangles (Oligons) that anchor macroscopic MFDM scalar field halos $\psi(x,t)$. In quantum mechanics, a scalar field of effective mass $m_\chi$ undergoes intrinsic quantum phase oscillations at its Compton frequency:

$$f_{\text{Compton}} = \frac{m_\chi c^2}{h}$$

Plugging in the empirical MFDM mass $m_\chi \approx 1.0 \times 10^{-22}\text{ eV}$ derived in Stream 3:

$$f_{\text{Compton}} = \frac{1.0 \times 10^{-22}\text{ eV}}{4.135667 \times 10^{-15}\text{ eV}\cdot\text{s}} \approx 2.418 \times 10^{-8}\text{ Hz} = 24.18\text{ nHz}$$

### 1.2 The Astrophysical Implication
The nanohertz band ($10^{-9}\text{ Hz} \le f \le 10^{-7}\text{ Hz}$) is precisely the frequency range probed by the NANOGrav 15-Year Pulsar Timing Array (PTA). Discrete $K_4$ Oligon halo oscillations and multiway hypergraph edge recombinations produce a gravitational wave hum with a sharp spectral bump centered at $24.18\text{ nHz}$, distinct from the smooth power-law emitted by supermassive black hole binaries.

---

## 2. The 4-Step Proof Protocol

```
+-----------------------------------------------------------------------------------+
+                    PHASE 1B SGWB ASTROPHYSICAL PROOF PIPELINE                     +
+                                                                                   +
+  1. Extract Strain Tensor ---> 2. Ingest NANOGrav 15yr ---> 3. Map Anisotropy    +
+     (dg_{\mu\nu}/dt, \gamma_oligon)    (Hellings-Downs, Posteriors)   (Angular C_\ell Sky Map) +
+                                                                 |                 +
+                                                                 v                 +
+                                                       4. Bayesian Selection       +
+                                                          (Bayes Factor B_10)      +
+-----------------------------------------------------------------------------------+
```

### Step 1: Extraction of Hypergraph GW Strain Tensor & Spectral Index
- **Objective:** Compute time-derivatives of the discrete metric tensor $g_{ij}(t)$ from 12-halo $N$-body merger checkpoints to derive the characteristic strain $h_c(f)$ and spectral index $\gamma_{\text{oligon}}$.
- **Mathematical Formulation:**
  The quadrupole momentum tensor $Q_{ij}$ of discrete $K_4$ defect clusters is given by:
  $$Q_{ij}(t) = \sum_{v \in V} M_t(v_i, v_j) \cdot x_i x_j - \frac{1}{3} \delta_{ij} \text{Tr}(M_t)$$
  The characteristic strain $h_c(f)$ scales as a power law $\Omega_{\text{GW}}(f) \propto f^{5 - \gamma}$.
- **Discriminator:**
  - Standard SMBHB Mergers: $\gamma_{\text{SMBHB}} = \frac{13}{3} \approx 4.33$.
  - $K_4$ Oligon Mergers: $\gamma_{\text{oligon}}$ predicted to feature a spectral slope shift near $f = 24.18\text{ nHz}$.

### Step 2: NANOGrav 15-Year Data Lake Ingestion (`data_benchmarks/nanograv_loader.py`)
- **Objective:** Download and parse official NANOGrav 15-year public data products into GCP Agora Data Lake (`gs://socrateai-datalake-gen-lang-client-0625573011/nanograv_15yr/`).
- **Data Products to Ingest:**
  1. **Hellings-Downs Curve:** Pulsar angular separation correlation $\Gamma(\xi)$.
  2. **Free-Spectrum Posteriors:** Per-frequency strain amplitude posterior distribution $A_{\text{GWB}}(f)$ across 14 frequency bins.
  3. **Timing Residuals:** Filtered timing residuals for 67 millisecond pulsars.

### Step 3: Angular Anisotropy & Topological Web Mapping (`nanograv_anisotropy.py`)
- **Objective:** Compute spherical harmonic coefficients $a_{\ell m}$ and angular power spectrum $C_\ell$ of $K_4$ Oligon cluster GW emission.
- **Physical Signature:**
  SMBHB backgrounds are predominantly isotropic ($\ell = 0$). $K_4$ Oligon clusters trace the cosmic web, producing non-zero multipoles $\ell = 2, 4, 6$ in the GW sky anisotropy map.

### Step 4: Bayesian Model Selection & Hypothesis Verification (`bayesian_sgwb_verifier.py`)
- **Objective:** Compute log-evidence $\ln Z$ and Bayes Factor $\mathcal{B}_{10}$ comparing:
  - **Hypothesis 0 ($\mathcal{H}_0$, Standard SMBHB):** $h_c(f) = A_{\text{GWB}} \left( \frac{f}{f_{\text{year}}} \right)^{(3 - \gamma)/2}$ with $\gamma = 4.33$.
  - **Hypothesis 1 ($\mathcal{H}_1$, Dual-Scale $K_4$ Oligon + Resonance):** $h_c(f) = A_{\text{GWB}} \left( \frac{f}{f_{\text{year}}} \right)^{(3 - \gamma_{\text{oligon}})/2} + A_{\text{res}} \exp\left( -\frac{(f - f_{\text{Compton}})^2}{2\sigma_f^2} \right)$.
- **Decision Rule:**
  - $\ln \mathcal{B}_{10} > 5.0$ $\implies$ **Decisive Evidence** supporting $K_4$ Oligon origin over standard SMBHB background.

---

## 3. Data Architecture & Module Interfaces

```text
hypergraph/
├── oligon_simulations/
│   └── gw_strain_extractor.py     # Step 1: Metric time derivative & h_c(f) spectrum
data_benchmarks/
├── nanograv_loader.py            # Step 2: GCP Data Lake ingestion for NANOGrav 15yr
scripts/
├── nanograv_anisotropy.py        # Step 3: Angular C_l power spectrum sky mapping
└── bayesian_sgwb_verifier.py     # Step 4: PyMC/Dynesty nested sampling & Bayes Factor
```

### Module Interface Specifications

#### A. `gw_strain_extractor.py`
```python
def extract_gw_strain_spectrum(checkpoint_dir: str) -> Dict[str, Any]:
    """
    Parses multi-halo merger checkpoints (checkpoint_step_*.pt),
    computes dM_t/dt, extracts quadrupole momentum tensor Q_ij(t),
    and returns characteristic strain h_c(f) and spectral index gamma_oligon.
    """
    pass
```

#### B. `nanograv_loader.py`
```python
def fetch_nanograv_15yr_data(gcs_bucket: str) -> Dict[str, str]:
    """
    Downloads NANOGrav 15-year dataset (Hellings-Downs, free-spectrum posteriors)
    and syncs to GCP Data Lake storage.
    """
    pass
```

#### C. `bayesian_sgwb_verifier.py`
```python
def compute_bayes_factor(
    nanograv_data: Dict[str, Any],
    hypergraph_spectrum: Dict[str, Any]
) -> Dict[str, float]:
    """
    Performs nested sampling / MCMC to compute evidence Z(H_0) and Z(H_1).
    Returns Bayes Factor ln(B_10) and BIC delta value.
    """
    pass
```

---

## 4. Implementation Plan & Definition of Done (DoD)

| Phase Milestone | Task Description | Target Deliverable | Acceptance Criteria |
|---|---|---|---|
| **Phase 1B.1** | Implement `gw_strain_extractor.py` | `hypergraph/oligon_simulations/gw_strain_extractor.py` | Extract $\gamma_{\text{oligon}}$ from $N$-body checkpoints |
| **Phase 1B.2** | Implement `nanograv_loader.py` | `data_benchmarks/nanograv_loader.py` | Ingest NANOGrav 15yr data into GCS bucket |
| **Phase 1B.3** | Implement `nanograv_anisotropy.py` | `scripts/nanograv_anisotropy.py` | Generate $C_\ell$ angular power spectrum map |
| **Phase 1B.4** | Implement `bayesian_sgwb_verifier.py` | `scripts/bayesian_sgwb_verifier.py` | Output Bayes Factor $\ln \mathcal{B}_{10}$ report |

---

## 5. Verification & Testing Strategy

1. **Unit Tests:** Verify `f_Compton` calculation equals $2.418 \times 10^{-8}\text{ Hz}$ given $m_\chi = 10^{-22}\text{ eV}$.
2. **Integration Tests:** Real-data validation test ensuring `proof_protocol_4step.py` correctly ingests the NANOGrav 15yr HD KDE posteriors (Lamb et al. 2023, Zenodo 10344086) and outputs calibrated $\Delta\text{BIC}$ and $\ln\mathcal{B}_{10}$ values consistent with the published free spectrum.
3. **Data Lake Sync:** Verify `gsutil` / `gcloud storage` syncs NANOGrav 15yr posteriors cleanly without corrupted JSON/FITS files.

---

**Approval:**  
*Document written as specification and implementation plan only. Code implementation deferred as instructed.*
