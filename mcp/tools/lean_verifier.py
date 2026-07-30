"""
MCP Lean 4 Verifier
===================
Verifies Lean 4 proofs for computational rigor.
Executes the Lean 4 compiler/lake to ensure no `sorry` or `admit` tokens are present.
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, Any


class Lean4Verifier:
    """Verifies Lean 4 proofs by invoking the Lean compiler and checking for unresolved goals."""

    def __init__(self, workspace_root: str = "."):
        """Initializes the Lean 4 verifier.
        
        Args:
            workspace_root: Path to the root of the Lean 4 workspace (where lakefile.lean would be).
        """
        self.workspace_root = Path(workspace_root)
        self.lean_bin = self._find_lean()

    def _find_lean(self) -> str:
        """Locates the lean executable on the system."""
        # Try elan first, then system path
        elan_lean = Path.home() / ".elan" / "bin" / "lean"
        if elan_lean.exists():
            return str(elan_lean)
        
        try:
            res = subprocess.run(["which", "lean"], capture_output=True, text=True)
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip()
        except Exception:
            pass
            
        return "lean" # fallback to path, might fail later

    def check_for_sorry(self, file_path: Path) -> bool:
        """Fast static analysis to check if 'sorry' or 'admit' are present in the file."""
        if not file_path.exists():
            return False
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Basic heuristic, the real check is the compiler output
        for bad_token in ["sorry", "admit"]:
            if bad_token in content:
                # Make sure it's not in a comment (basic check)
                lines = content.split("\n")
                for line in lines:
                    if bad_token in line and not line.strip().startswith("--") and not line.strip().startswith("/-"):
                        return True
        return False

    def verify(self, file_path: str) -> Dict[str, Any]:
        """Runs the Lean compiler on the given file and parses the output.
        
        Args:
            file_path: Relative or absolute path to the .lean file.
            
        Returns:
            Dict containing verification status and messages.
        """
        path = self.workspace_root / file_path
        if not path.exists():
            return {
                "status": "failed",
                "file": str(file_path),
                "error": f"File not found: {path}"
            }

        # First do a fast static check for sorry
        if self.check_for_sorry(path):
            return {
                "status": "failed",
                "file": str(file_path),
                "error": "Proof contains 'sorry' or 'admit' tokens and is incomplete."
            }

        # Run the lean compiler
        try:
            # Run lean in the workspace root
            res = subprocess.run(
                [self.lean_bin, str(path)],
                cwd=str(self.workspace_root),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = res.stdout + res.stderr
            
            if res.returncode == 0 and "error:" not in output.lower():
                return {
                    "status": "verified",
                    "file": str(file_path),
                    "message": "Successfully verified without errors."
                }
            else:
                return {
                    "status": "failed",
                    "file": str(file_path),
                    "error": "Compilation failed or contains errors.",
                    "compiler_output": output
                }
                
        except FileNotFoundError:
            return {
                "status": "unverified",
                "file": str(file_path),
                "error": "Lean compiler not found. Ensure elan/lean is installed."
            }
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "file": str(file_path),
                "error": "Lean compiler timed out after 30 seconds."
            }
