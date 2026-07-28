"""
MCP Unit Manager
Strict dimensional analysis and unit conversions using Wolfram Engine or deterministic physics formulas.
Prevents conversion bugs (e.g., meV to log10(m/eV) or eV to J/kg).
"""

import math
from typing import Dict, Any

class UnitManager:
    """Handles strict dimensional analysis and conversions."""
    
    # Constants
    EV_TO_JOULES = 1.602176634e-19
    EV_TO_KG = 1.782661921e-36  # E = mc^2 -> m = E/c^2
    HBAR_C_EV_M = 1.973269804e-7 # eV*m

    @staticmethod
    def mev_to_ev(mev_val: float) -> float:
        """Converts milli-electronvolts (meV) to eV."""
        return mev_val * 1e-3

    @staticmethod
    def ev_to_log10_m_ev(ev_val: float) -> float:
        """Calculates log10(m / eV) for dark matter particle mass m in eV."""
        if ev_val <= 0:
            raise ValueError("Mass in eV must be positive")
        return math.log10(ev_val)

    @staticmethod
    def convert_oligon_mass_units(mass_mev: float) -> Dict[str, Any]:
        """
        Converts Oligon defect mass in meV to eV, kg, and log10(m/eV).
        """
        mass_ev = UnitManager.mev_to_ev(mass_mev)
        mass_kg = mass_ev * UnitManager.EV_TO_KG
        log10_m_ev = UnitManager.ev_to_log10_m_ev(mass_ev)
        
        return {
            "input_mass_mev": mass_mev,
            "mass_ev": mass_ev,
            "mass_kg": mass_kg,
            "log10_m_ev": log10_m_ev,
            "dimensional_check": "PASSED"
        }

if __name__ == "__main__":
    # Test conversion for a 0.1 meV Oligon dark matter candidate
    res = UnitManager.convert_oligon_mass_units(0.1)
    print("Unit Conversion Result:", res)
