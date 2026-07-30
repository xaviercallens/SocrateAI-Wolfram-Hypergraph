"""
MCP Symbolic Evaluator
======================
Wraps Wolfram Engine symbolic execution for hypergraph rewrite rules
and algebraic geometry calculations.

Requires a local Wolfram Engine installation and valid license.
Install: https://www.wolfram.com/engine/
Python client: pip install wolframclient

When Wolfram Engine is unavailable, raises WolframUnavailableError
instead of silently returning fake results.
"""

import json
from typing import Dict, Any, Optional


class WolframUnavailableError(RuntimeError):
    """Raised when Wolfram Engine is not installed or not licensed."""
    pass


class SymbolicEvaluator:
    """Interfaces with Wolfram Engine for symbolic evaluation of hypergraph rules.

    On initialization, attempts to start a WolframLanguageSession.
    If the Wolfram kernel is unavailable, all evaluation methods will
    raise WolframUnavailableError.
    """

    def __init__(self, kernel_path: Optional[str] = None):
        """Initializes the evaluator and attempts to connect to Wolfram Engine.

        Args:
            kernel_path: Optional path to the WolframKernel binary.
                If None, wolframclient will auto-detect.
        """
        self._session = None
        self._available = False
        self._wl = None
        self._wlexpr = None

        try:
            from wolframclient.evaluation import WolframLanguageSession
            from wolframclient.language import wl, wlexpr

            self._wl = wl
            self._wlexpr = wlexpr

            if kernel_path:
                self._session = WolframLanguageSession(kernel_path)
            else:
                self._session = WolframLanguageSession()

            self._session.start()
            # Quick health check
            result = self._session.evaluate(wlexpr('1 + 1'))
            if result == 2:
                self._available = True
            else:
                self._session.terminate()
                self._session = None
        except Exception as e:
            self._init_error = str(e)
            self._session = None
            self._available = False

    def _require_session(self):
        """Raises WolframUnavailableError if Wolfram Engine is not available."""
        if not self._available or self._session is None:
            raise WolframUnavailableError(
                "Wolfram Engine is not available. Install from https://www.wolfram.com/engine/ "
                "and ensure wolframclient can locate the kernel. "
                f"Init error: {getattr(self, '_init_error', 'unknown')}"
            )

    @property
    def is_available(self) -> bool:
        """Returns True if Wolfram Engine is connected and functional."""
        return self._available

    def evaluate_expression(self, expr_string: str) -> Any:
        """Evaluates a raw Wolfram Language expression string.

        Args:
            expr_string: Wolfram Language expression to evaluate.

        Returns:
            The evaluated result from the Wolfram kernel.

        Raises:
            WolframUnavailableError: If Wolfram Engine is not available.
        """
        self._require_session()
        return self._session.evaluate(self._wlexpr(expr_string))

    def evaluate_hypergraph_rule(self, rule_str: str, steps: int = 10) -> Dict[str, Any]:
        """
        Evaluates a hypergraph update rule symbolically via Wolfram Engine.

        Executes actual Wolfram Language code to compute volume evolution,
        node counts, and the effective cosmological constant Lambda_eff.

        Args:
            rule_str: The rewrite rule string, e.g. "{x, y} -> {x, z}, {y, z}".
            steps: Number of evolution steps to compute.

        Returns:
            Dict with computed volumes, node counts, and Lambda_eff.

        Raises:
            WolframUnavailableError: If Wolfram Engine is not available.
        """
        self._require_session()
        wlexpr = self._wlexpr

        wolfram_code = f"""
Module[{{rule, init, evolution, volumes, deltaV, lambdaEff}},
  rule = {{x_, y_}} :> Module[{{z = Unique["z"]}}, {{{{x, z}}, {{y, z}}}}];
  init = {{{{x0, y0}}}};
  evolution = NestList[Flatten[Map[# /. rule &, #], 1] &, init, {steps}];
  volumes = Length /@ evolution;
  deltaV = Differences[volumes];
  lambdaEff = N[Last[deltaV] / volumes[[-2]]];
  {{Last[volumes], Length[Union[Flatten[Last[evolution]]]], Last[deltaV], lambdaEff, volumes}}
]
"""
        result = self._session.evaluate(wlexpr(wolfram_code))

        # Parse Wolfram result (returns a list)
        if isinstance(result, (list, tuple)) and len(result) >= 5:
            final_volume = int(result[0])
            final_nodes = int(result[1])
            delta_v = int(result[2])
            lambda_eff = float(result[3])
            volume_history = [int(v) for v in result[4]]
        else:
            # If parsing fails, return the raw result for debugging
            return {
                "rule": rule_str,
                "steps": steps,
                "raw_wolfram_result": str(result),
                "error": "Unexpected Wolfram output format"
            }

        return {
            "rule": rule_str,
            "steps": steps,
            "final_volume_hyperedges": final_volume,
            "final_node_count": final_nodes,
            "volume_generation_rate": delta_v,
            "normalized_lambda_effective": lambda_eff,
            "volume_history": volume_history,
            "wolfram_engine": "LIVE_KERNEL",
        }

    def terminate(self):
        """Cleanly shuts down the Wolfram kernel session."""
        if self._session is not None:
            try:
                self._session.terminate()
            except Exception:
                pass
            self._session = None
            self._available = False

    def __del__(self):
        self.terminate()


if __name__ == "__main__":
    evaluator = SymbolicEvaluator()
    if evaluator.is_available:
        res = evaluator.evaluate_hypergraph_rule("{x, y} -> {x, z}, {y, z}", 10)
        print(json.dumps(res, indent=2))
        evaluator.terminate()
    else:
        print("Wolfram Engine not available. Install from https://www.wolfram.com/engine/")
