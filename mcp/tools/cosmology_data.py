"""
MCP Cosmology Data Tool
Provides deterministic access to astrophysical and cosmological data (CosmologyData[], FormulaData[]).
"""

from typing import Dict, Any

class CosmologyDataTool:
    """Wrapper for cosmological parameters and formulas."""

    @staticmethod
    def get_planck_cosmology_params() -> Dict[str, Any]:
        """Returns standard Planck cosmological parameters."""
        return {
            "H0_km_s_Mpc": 67.4,
            "Omega_b": 0.0493,
            "Omega_cdm": 0.264,
            "Omega_Lambda": 0.6847,
            "rho_critical_g_cm3": 8.53e-30,
            "rho_lambda_eV4": 2.4e-3  # meV^4 scale
        }

    @staticmethod
    def calculate_oligon_dark_matter_density(oligon_mass_mev: float, defect_density_m3: float) -> Dict[str, Any]:
        """Calculates energy density of Oligon topological defects."""
        mass_ev = oligon_mass_mev * 1e-3
        mass_kg = mass_ev * 1.782661921e-36
        energy_joules = mass_kg * (299792458 ** 2)
        
        rho_energy_j_m3 = energy_joules * defect_density_m3
        rho_crit = 8.53e-27 # kg/m^3 -> J/m^3
        
        return {
            "oligon_mass_mev": oligon_mass_mev,
            "defect_density_m3": defect_density_m3,
            "energy_density_j_m3": rho_energy_j_m3,
            "omega_oligon_fraction": rho_energy_j_m3 / (rho_crit * (299792458 ** 2))
        }

if __name__ == "__main__":
    tool = CosmologyDataTool()
    print("Planck Params:", tool.get_planck_cosmology_params())
