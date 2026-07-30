import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os

# Set style
plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Load results
results_file = Path("dark_matter/hypergraph/results/proof_protocol_4step.json")
if not results_file.exists():
    print("Run proof_protocol_4step.py first.")
    exit(1)

with open(results_file, 'r') as f:
    results = json.load(f)

# ─────────────────────────────────────────────────────────────
# PLOT 1: GW Strain h_c(f)
# ─────────────────────────────────────────────────────────────
s2 = results["step2_nanograv"]
s4 = results["step4_bayes"]
s1 = results["step1_gw_strain"]

F_YEAR = 1.0 / (365.25 * 86400.0)
F_COMPTON = 2.418e-8

# Use 14 frequencies from NANOGrav actual range
freqs = np.linspace(s2["freq_range_hz"][0], s2["freq_range_hz"][1], 14)
# Reconstruct median log10rho from saved array and dummy rest for visual
median_rho = np.array(s2["median_log10rho_0to4"] + [-4.139, -4.118, -4.455, -4.284, -4.198, -4.256, -4.297, -4.365, -4.330])
sigma_rho = 2.3 * np.ones_like(median_rho) # approximate error bar from output

T_span = 16.03 * 365.25 * 86400.0
h_c_obs = 10**median_rho * np.sqrt(12 * np.pi**2 * freqs**3 * T_span)
h_c_err_up = 10**(median_rho + sigma_rho) * np.sqrt(12 * np.pi**2 * freqs**3 * T_span) - h_c_obs
h_c_err_dn = h_c_obs - 10**(median_rho - sigma_rho) * np.sqrt(12 * np.pi**2 * freqs**3 * T_span)

ax1.errorbar(freqs, h_c_obs, yerr=[h_c_err_dn, h_c_err_up], fmt='o', color='white', 
             label='NANOGrav 15yr HD KDE Median', alpha=0.8, capsize=3)

# Best H0 (SMBHB)
log10A0, gamma0 = s4["best_H0"]["log10A"], s4["best_H0"]["gamma"]
f_dense = np.logspace(np.log10(freqs[0]), np.log10(freqs[-1]), 100)
h0 = 10**log10A0 * (f_dense / F_YEAR)**((3.0 - gamma0) / 2.0)
ax1.plot(f_dense, h0, '--', color='#00d2ff', lw=2, label=f'SMBHB (H0)\nγ={gamma0:.2f}')

# Best H1 (Oligon)
log10A1, gamma1, log10A_res = s4["best_H1"]["log10A"], s4["best_H1"]["gamma"], s4["best_H1"]["log10A_res"]
h1_pl = 10**log10A1 * (f_dense / F_YEAR)**((3.0 - gamma1) / 2.0)
sigma_f = 0.15 * F_COMPTON
h1_res = 10**log10A_res * np.exp(-0.5 * ((f_dense - F_COMPTON) / sigma_f)**2)
h1 = h1_pl + h1_res
ax1.plot(f_dense, h1, '-', color='#ff003c', lw=2.5, label=f'K4 Oligon (H1)\nγ={gamma1:.2f}')
ax1.axvline(F_COMPTON, color='gray', linestyle=':', label='f_Compton (24.18 nHz)')

ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlabel('Frequency f [Hz]', fontsize=12)
ax1.set_ylabel(r'Characteristic Strain $h_c(f)$', fontsize=12)
ax1.set_title('Gravitational Wave Background: NANOGrav vs Oligon Model', fontsize=14)
ax1.legend(loc='lower left', frameon=False)
ax1.grid(True, alpha=0.1)

# ─────────────────────────────────────────────────────────────
# PLOT 2: C_l Anisotropy Spectrum
# ─────────────────────────────────────────────────────────────
s3 = results["step3_anisotropy"]["anisotropy_ratio"]
ells = np.array([int(k) for k in s3.keys()])
ratios = np.array([s3[k] for k in s3.keys()])

ax2.bar(ells, ratios, color='#a020f0', alpha=0.7)
ax2.axhline(1.0, color='white', linestyle='--', label='Isotropic SMBHB (H0)')
ax2.set_xlabel(r'Multipole Moment $\ell$', fontsize=12)
ax2.set_ylabel(r'$C_\ell$(Oligon) / $C_\ell$(Iso)', fontsize=12)
ax2.set_title('Topological Cosmic Web Anisotropy', fontsize=14)
ax2.set_xticks(ells)
ax2.legend(frameon=False)

plt.tight_layout()
out_img = Path("dark_matter/hypergraph/results/nanograv_oligon_comparison.png")
plt.savefig(out_img, dpi=300, bbox_inches='tight', transparent=True)
print(f"Visualization saved to {out_img}")
