"""
Planck CMB Power Spectrum Data Loader
=====================================
Loads real Planck 2018 CMB power spectrum datasets for hypergraph benchmarking.
Requires actual data files — raises FileNotFoundError instead of generating synthetic spectra.

Data acquisition:
  Download from Planck Legacy Archive: https://pla.esac.esa.int/
  Required file: COM_PowerSpect_CMB-TT-full_R3.01.txt (or equivalent)
  Set PLANCK_DATA_DIR env var or pass data_dir to constructor.
"""

import os
import numpy as np
from typing import Optional


# URL for automated download (Planck Legacy Archive public files)
PLANCK_TT_URL = "https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/COM_PowerSpect_CMB-TT-full_R3.01.txt"


class PlanckDataLoader:
    """Loads Planck CMB power spectrum datasets for hypergraph benchmarking."""

    def __init__(self, data_dir: Optional[str] = None):
        """Initializes the Planck data loader.

        Args:
            data_dir (str, optional): Base directory for Planck data.
                Falls back to PLANCK_DATA_DIR env var, then raises ValueError.
        """
        self.data_dir = data_dir or os.environ.get("PLANCK_DATA_DIR")
        if self.data_dir is None:
            raise ValueError(
                "Planck data directory must be specified via constructor argument or "
                "PLANCK_DATA_DIR environment variable. Download Planck 2018 power spectra "
                "from https://pla.esac.esa.int/ and set the path accordingly."
            )

    def load_cmb_power_spectrum(self, filename: str = "planck_tt_te_ee.txt") -> dict:
        """Loads TT, TE, EE CMB power spectra from Planck data files.

        Args:
            filename (str, optional): Filename of the Planck spectra text file.
                Defaults to "planck_tt_te_ee.txt".

        Returns:
            dict: Dictionary with 'ell', 'TT', 'TE', 'EE' array keys.

        Raises:
            FileNotFoundError: If the Planck data file does not exist.
            ValueError: If the file format is unrecognized.
        """
        path = os.path.join(self.data_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Planck CMB power spectrum file not found: {path}\n"
                f"Download from {PLANCK_TT_URL}\n"
                f"or from https://pla.esac.esa.int/ and place in {self.data_dir}/"
            )

        # Load data, skipping comment lines (Planck files use '#' comments)
        data = np.loadtxt(path, comments='#')

        if data.ndim != 2 or data.shape[1] < 2:
            raise ValueError(
                f"Unexpected Planck data format in {path}: shape={data.shape}. "
                f"Expected at least 2 columns (ell, D_ell^TT)."
            )

        result = {"ell": data[:, 0]}
        result["TT"] = data[:, 1]
        if data.shape[1] > 2:
            result["TE"] = data[:, 2]
        if data.shape[1] > 3:
            result["EE"] = data[:, 3]

        return result
