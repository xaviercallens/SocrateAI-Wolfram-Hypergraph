import numpy as np

class SKAPTALoader:
    EXPECTED_RELEASES = {
        "ska_dr1": {"url": "https://ska-telescope.org/data/pta/dr1/", "expected_date": "2027-Q2", "expected_bins": 30},
        "ipta_dr3": {"url": "https://ipta4gw.org/data/dr3/", "expected_date": "2027-Q1", "expected_bins": 14},
    }

    def __init__(self, data_dir: str = "/tmp/ska_data/", release: str = "ska_dr1"):
        self.data_dir = data_dir
        self.release = release
        if self.release not in self.EXPECTED_RELEASES:
            raise ValueError(f"Unknown release {release}")

    def download_free_spectrum(self):
        """Downloads the free spectrum from the configured URL."""
        expected_date = self.EXPECTED_RELEASES[self.release]["expected_date"]
        raise NotImplementedError(f"{self.release.upper()} not yet released. Expected: {expected_date}")

    def load_free_spectrum(self) -> dict:
        """Parses the expected SKA format."""
        file_path = f"{self.data_dir}/{self.release}_free_spectrum.npz"
        try:
            data = np.load(file_path)
            frequencies = data["frequencies_hz"]
            posteriors = data["log10_rho_posteriors"]
            
            self.validate_format(frequencies, posteriors)
            
            return {
                "frequencies_hz": frequencies,
                "amplitude_matrix": posteriors,
                "num_bins": len(frequencies),
                "release": self.release
            }
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found at {file_path}. Did you call download_free_spectrum()?")
        
    def validate_format(self, frequencies: np.ndarray, posteriors: np.ndarray):
        """Checks array shapes and raises ValueError if wrong."""
        expected_bins = self.EXPECTED_RELEASES[self.release]["expected_bins"]
        if len(frequencies) != expected_bins:
            raise ValueError(f"Expected {expected_bins} frequency bins, got {len(frequencies)}")
        
        if len(posteriors.shape) != 2:
            raise ValueError(f"Expected 2D array for posteriors, got {len(posteriors.shape)}D")
            
        if posteriors.shape[1] != expected_bins:
            raise ValueError(f"Expected {expected_bins} columns in posteriors, got {posteriors.shape[1]}")

    def compute_spectral_index(self, frequencies: np.ndarray, posteriors: np.ndarray) -> float:
        """Fits power-law log10_rho ~ α * log10(f) + β to the median spectrum."""
        median_rho = np.median(posteriors, axis=0)
        log_f = np.log10(frequencies)
        
        # Polyfit returns [alpha, beta]
        alpha, _ = np.polyfit(log_f, median_rho, 1)
        
        # h_c ~ f^((3-gamma)/2), and rho ~ h_c^2 / f^3 -> rho ~ f^(-gamma)
        # So log10_rho ~ -gamma * log10(f)
        gamma = -alpha
        return gamma
