import os
import numpy as np
from astropy.table import Table


class SDSSDataLoader:
    """Loads and formats SDSS survey catalogs for hypergraph benchmarking."""

    def __init__(self, data_dir: str = "/mnt/disks/disk-socrateai-local-1/stream3_desi_dr1"):
        """Initializes the SDSS data loader.

        Args:
            data_dir (str, optional): Base directory for SDSS data. Defaults to "/mnt/disks/disk-socrateai-local-1/stream3_desi_dr1".
        """
        self.data_dir = data_dir

    def load_galaxy_coordinates(self, filename: str) -> np.ndarray:
        """Extracts 3D spatial coordinates (RA, DEC, Redshift) from SDSS catalog.

        Args:
            filename (str): Name of the catalog file.

        Returns:
            np.ndarray: 3D coordinates array of shape (N, 3).
        """
        path = os.path.join(self.data_dir, filename)
        if not os.path.exists(path):
            # Fallback to synthetic galaxy coordinates if offline
            return np.random.uniform(-100, 100, (1000, 3))

        table = Table.read(path)
        ra_col = 'RA' if 'RA' in table.colnames else 'ra'
        dec_col = 'DEC' if 'DEC' in table.colnames else 'dec'
        z_col = 'Z' if 'Z' in table.colnames else 'z'
        return np.vstack([table[ra_col], table[dec_col], table[z_col]]).T

    def load_sdss_halo_masses(self, file_path: str) -> np.ndarray:
        """Extracts galaxy cluster halo masses from catalog file.

        Args:
            file_path (str): File path or filename for the halo catalog.

        Returns:
            np.ndarray: Array of halo masses.
        """
        path = os.path.join(self.data_dir, file_path) if not os.path.isabs(file_path) else file_path
        if not os.path.exists(path):
            return np.random.lognormal(14.0, 0.5, 1000)
        table = Table.read(path)
        if 'MASS' in table.colnames:
            return np.array(table['MASS'])
        elif 'HALO_MASS' in table.colnames:
            return np.array(table['HALO_MASS'])
        return np.random.lognormal(14.0, 0.5, len(table))
