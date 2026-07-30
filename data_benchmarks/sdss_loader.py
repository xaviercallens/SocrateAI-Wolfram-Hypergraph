"""
SDSS Galaxy Survey Data Loader
==============================
Loads and formats SDSS survey catalogs for hypergraph benchmarking.
Requires real data files — raises FileNotFoundError instead of generating synthetic fallbacks.

Data acquisition:
  Download SDSS DR18 catalogs from https://www.sdss.org/dr18/
  or use CasJobs at https://skyserver.sdss.org/casjobs/
  Place files in the directory specified by SDSS_DATA_DIR env var or constructor argument.
"""

import os
import numpy as np
from typing import Optional
from astropy.table import Table


class SDSSDataLoader:
    """Loads and formats SDSS survey catalogs for hypergraph benchmarking."""

    def __init__(self, data_dir: Optional[str] = None):
        """Initializes the SDSS data loader.

        Args:
            data_dir (str, optional): Base directory for SDSS data.
                Falls back to SDSS_DATA_DIR env var, then raises ValueError.
        """
        self.data_dir = data_dir or os.environ.get("SDSS_DATA_DIR")
        if self.data_dir is None:
            raise ValueError(
                "SDSS data directory must be specified via constructor argument or "
                "SDSS_DATA_DIR environment variable. Download SDSS DR18 catalogs from "
                "https://www.sdss.org/dr18/ and set the path accordingly."
            )

    def load_galaxy_coordinates(self, filename: str) -> np.ndarray:
        """Extracts 3D spatial coordinates (RA, DEC, Redshift) from SDSS catalog.

        Args:
            filename (str): Name of the catalog file (FITS format).

        Returns:
            np.ndarray: 3D coordinates array of shape (N, 3).

        Raises:
            FileNotFoundError: If the catalog file does not exist.
        """
        path = os.path.join(self.data_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"SDSS catalog not found: {path}\n"
                f"Download from https://www.sdss.org/dr18/ and place in {self.data_dir}/"
            )

        table = Table.read(path)
        ra_col = 'RA' if 'RA' in table.colnames else 'ra'
        dec_col = 'DEC' if 'DEC' in table.colnames else 'dec'
        z_col = 'Z' if 'Z' in table.colnames else 'z'

        for col in [ra_col, dec_col, z_col]:
            if col not in table.colnames:
                raise KeyError(
                    f"Required column '{col}' not found in {filename}. "
                    f"Available columns: {table.colnames}"
                )

        return np.vstack([table[ra_col], table[dec_col], table[z_col]]).T

    def load_sdss_halo_masses(self, file_path: str) -> np.ndarray:
        """Extracts galaxy cluster halo masses from catalog file.

        Args:
            file_path (str): File path or filename for the halo catalog.

        Returns:
            np.ndarray: Array of halo masses.

        Raises:
            FileNotFoundError: If the halo catalog file does not exist.
            KeyError: If no recognized mass column is found.
        """
        path = os.path.join(self.data_dir, file_path) if not os.path.isabs(file_path) else file_path
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"SDSS halo catalog not found: {path}\n"
                f"Download from https://www.sdss.org/dr18/ and place in {self.data_dir}/"
            )

        table = Table.read(path)
        if 'MASS' in table.colnames:
            return np.array(table['MASS'])
        elif 'HALO_MASS' in table.colnames:
            return np.array(table['HALO_MASS'])
        else:
            raise KeyError(
                f"No recognized mass column ('MASS' or 'HALO_MASS') found in {path}. "
                f"Available columns: {table.colnames}"
            )
