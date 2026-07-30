(* Wolfram Language MFDM Mass Spectrum Trial *)
vacuumRate = {vacuum_expansion_rate_H};
k3Edges = 3; k4Edges = 6; k5Edges = 10;

k3Integrity = Table[k3Edges + (0.8 - vacuumRate) * t, {t, 0, {iterations}}];
k4Integrity = Table[k4Edges + (1.5 - vacuumRate) * t, {t, 0, {iterations}}];
k5Integrity = Table[k5Edges + (3.2 - vacuumRate) * t, {t, 0, {iterations}}];

Print["K3 Final Integrity: ", Last[k3Integrity], " -> Dissolved by Dark Energy"];
Print["K4 Final Integrity: ", Last[k4Integrity], " -> Stable MFDM Soliton Threshold"];
Print["K5 Final Integrity: ", Last[k5Integrity], " -> Ultra-Dense Core"];

{{Last[k3Integrity], Last[k4Integrity], Last[k5Integrity]}}
