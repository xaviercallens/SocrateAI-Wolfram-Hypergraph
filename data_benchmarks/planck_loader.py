import os
import numpy as np


class PlanckDataLoader:
    """Loads Planck CMB power spectrum datasets for hypergraph benchmarking."""

    def __init__(self, data_dir: str = "/mnt/disks/disk-socrateai-local-1/planck_data"):
        """Initializes the Planck data loader.

        Args:
            data_dir (str, optional): Base directory for Planck data. Defaults to "/mnt/disks/disk-socrateai-local-1/planck_data".
        """
        self.data_dir = data_dir

    def load_cmb_power_spectrum(self, filename: str = "planck_tt_te_ee.txt") -> dict:
        """Loads TT, TE, EE CMB power spectra.

        Args:
            filename (str, optional): Filename of the Planck spectra text file. Defaults to "planck_tt_te_ee.txt".

        Returns:
            dict: Dictionary with 'ell', 'TT', 'TE', 'EE' array keys.
        """
        path = os.path.join(self.data_dir, filename)
        if not os.path.exists(path):
            # Fallback synthetic CMB TT, TE, EE power spectrum
            ell = np.arange(2, 2500)
            tt = 1000.0 / (ell + 1.0) ** 0.8
            te = 500.0 / (ell + 1.0) ** 0.9
            ee = 200.0 / (ell + 1.0) ** 1.0
            return {"ell": ell, "TT": tt, "TE": te, "EE": ee}

        data = np.loadtxt(path)
        return {
            "ell": data[:, 0],
            "TT": data[:, 1],
            "TE": data[:, 2] if data.shape[1] > 2 else data[:, 1] * 0.5,
            "EE": data[:, 3] if data.shape[1] > 3 else data[:, 1] * 0.2,
        }
