# Scientific Review Brief: Phase 1B NANOGrav 15-Year Data Verification & $K_4$ Oligon Proof
**Date:** July 30, 2026 (Updated)  
**Subject:** Real-Data Extraction and Bayesian Model Selection Against Official NANOGrav 15-Year HD Free Spectrum  
**Author:** HyperGraphAstro Pipeline Lead  
**Target:** Google DeepMind / Deep Think Review Board  

## Executive Summary
This brief details the execution of the Phase 1B Experimental Protocol. Following the theoretical prediction that Mixed-Fraction Fuzzy Dark Matter (MFDM) halos anchored by $K_4$ Oligons oscillate at a Compton Frequency of $f_{\text{Compton}} = 24.18\text{ nHz}$ (for $m_\chi = 1.0 \times 10^{-22}\text{ eV}$), we performed an independent verification using the publicly released **NANOGrav 15-Year Dataset**.

**Critical Update:** The analysis is now performed exclusively against real observational data. All synthetic fallbacks have been removed. The Bayesian result is **inconclusive** ($\ln\mathcal{B}_{10} = 1.41$) — not decisive — and we report it honestly as such.

## Data Acquisition & Certification
The data products were acquired directly from the official NANOGrav public archives:
- **Source:** Zenodo record 10344086 — "KDE Representations of the Gravitational Wave Background Free Spectra Present in the NANOGrav 15-Year Dataset" (Lamb et al. 2023, PRD 108, 103019).
- **Primary Data Products:** 30-frequency bin Hellings-Downs correlated free spectrum KDE posteriors (`30f_fs{hd}_ceffyl/`), containing `freqs.npy`, `density.npy` (shape: 1×30×10000), and `log10rhogrid.npy` (10000-point shared grid).
- **Data Integrity:** All loaders (`data_benchmarks/nanograv_loader.py`) raise `FileNotFoundError` when data files are absent. Zero `np.random` calls exist in any production data path.

## Analysis Pipeline (4-Step Proof Protocol)

### Step 1: Hypergraph GW Strain Extraction
- Simulated a 12-node, 3-cluster $K_4$ merger (40 sparse tensor evolution steps)
- Extracted quadrupole second time derivative $\ddot{Q}(t)$ → FFT → characteristic strain $h_c(f)$
- **Result:** $\gamma_{\text{oligon}} = 4.85$, compared to $\gamma_{\text{SMBHB}} = 4.33$ → **$\Delta\gamma = 0.51$ (falsifiable signature)**

### Step 2: Real NANOGrav Data Ingestion
- Loaded 30-bin HD-correlated free spectrum from Lamb et al. 2023
- Frequency range: $1.98 \times 10^{-9}$ to $5.93 \times 10^{-8}$ Hz
- $f_{\text{Compton}} = 24.18$ nHz falls in frequency bin ~11

### Step 3: Cosmic Web Anisotropy Mapping
- Computed angular power spectrum $C_\ell$ via spherical harmonic decomposition
- **Result:** $l=4$ multipole shows $C_\ell(\text{Oligon})/C_\ell(\text{Iso}) = 16.07$ — strong octopole anisotropy

### Step 4: Bayesian Model Selection
- Performed in $\log_{10}(\rho)$ space, directly matching KDE posterior medians
- 14 frequency bins, grid search over calibrated priors

| Metric | $\mathcal{H}_0$ (SMBHB) | $\mathcal{H}_1$ (K4 Oligon) |
|---|---|---|
| $\log\mathcal{L}_{\max}$ | $-13.82$ | $-11.09$ |
| BIC | $32.92$ | **$30.10$** |
| $\Delta$BIC | — | **$-2.83$ (marginally favors $\mathcal{H}_1$)** |
| $\ln\mathcal{B}_{10}$ | — | $1.41$ |

**VERDICT:** INCONCLUSIVE — $\mathcal{H}_1$ is marginally preferred but does not reach the $|\Delta\text{BIC}| > 6$ threshold for strong evidence. Definitive resolution requires SKA/IPTA sensitivity.

## Falsifiable Predictions
1. **Spectral Index:** $\gamma_{\text{oligon}} = 4.85 \neq 4.33$ (resolvable by SKA PTA at $\pm 0.1$ precision)
2. **Compton Resonance:** Excess at $f = 24.18 \pm 3.6$ nHz above the power-law continuum
3. **$l=4$ Anisotropy:** Persistent $l=4$ enhancement with $> 100$ pulsars

## Reproducibility
```bash
export NANOGRAV_CEFFYL_DIR=/tmp/nanograv_data/ceffyl_data
PYTHONPATH=. python3 scripts/proof_protocol_4step.py
```
All code: https://github.com/xaviercallens/SocrateAI-Wolfram-Hypergraph
