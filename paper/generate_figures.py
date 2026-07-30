import numpy as np
import matplotlib.pyplot as plt
import os

# Ensure we're in the right directory
os.makedirs('paper/figures', exist_ok=True)

# 1. Compton Resonance Figure
freqs = np.linspace(1e-9, 1e-7, 100)
f_year = 1.0 / (365.25 * 86400.0)
f_compton = 2.418e-8
sigma_f = 0.15 * f_compton

h_c_smbhb = 2.4e-15 * (freqs / f_year) ** ((3.0 - 4.33) / 2.0)
h_c_resonance = 1.5e-15 * np.exp(-0.5 * ((freqs - f_compton) / sigma_f) ** 2)
h_c_total = h_c_smbhb + h_c_resonance

plt.figure(figsize=(8, 5))
plt.plot(freqs * 1e9, h_c_smbhb * 1e15, 'k--', label='Hypothesis 0 (SMBHB Background)')
plt.plot(freqs * 1e9, h_c_total * 1e15, 'r-', linewidth=2, label='Hypothesis 1 ($K_4$ Oligon + Resonance)')
plt.axvline(f_compton * 1e9, color='blue', linestyle=':', label='$f_{Compton} = 24.18$ nHz')
plt.xlabel('Frequency [nHz]')
plt.ylabel('Characteristic Strain $h_c(f)$ [$10^{-15}$]')
plt.title('SGWB Characteristic Strain: SMBHB vs $K_4$ Oligon Model')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('paper/figures/fig_compton_resonance.png', dpi=300)
plt.close()

# 2. Angular Power Spectrum C_l Figure
l_vals = np.array([0, 1, 2, 3, 4, 5, 6])
c_l_iso = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
c_l_oligon = np.array([1.0, 0.01, 0.146, 0.005, 0.023, 0.001, 0.002])

plt.figure(figsize=(8, 5))
plt.plot(l_vals, c_l_iso, 'ks-', markersize=8, label='Isotropic SMBHB')
plt.plot(l_vals, c_l_oligon, 'ro-', markersize=8, label='$K_4$ Cosmic Web')
plt.yscale('log')
plt.xlabel('Multipole $\ell$')
plt.ylabel('Angular Power $C_\ell$')
plt.title('Angular Power Spectrum of SGWB Anisotropy')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('paper/figures/fig_angular_power.png', dpi=300)
plt.close()

# 3. Bayesian Model Selection Bar Chart
models = ['$\mathcal{H}_0$ (SMBHB)', '$\mathcal{H}_1$ ($K_4$ Oligon)']
bic_vals = [-930.74, -946.48]

plt.figure(figsize=(6, 5))
bars = plt.bar(models, bic_vals, color=['gray', 'red'])
plt.ylabel('Bayesian Information Criterion (BIC)')
plt.title('Model Selection (Lower BIC is better)')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval - 5, f'{yval}', ha='center', va='top', color='white', fontweight='bold')
plt.tight_layout()
plt.savefig('paper/figures/fig_bayesian_bic.png', dpi=300)
plt.close()

print("Figures generated successfully in paper/figures/")
