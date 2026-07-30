(* Wolfram Language Simultaneous K3/K4/K5 Mass Spectrum Trial with Isomorphic Pruning *)
k3Seed = {{1, 2}, {2, 3}, {3, 1}};
k4Seed = {{10, 11}, {11, 12}, {12, 10}, {10, 13}, {11, 13}, {12, 13}};
k5Seed = {{20, 21}, {21, 22}, {22, 23}, {23, 24}, {24, 20}, {20, 22}, {21, 23}, {22, 24}, {23, 20}, {24, 21}};

initHypergraph = Union[k3Seed, k4Seed, k5Seed];

ruleA = {{x_, y_}, {x_, z_}} :> {{x, w}, {y, w}, {z, w}};
ruleB = {{x_, y_}, {y_, z_}, {z_, x_}} :> {{x, y}, {y, z}, {z, x}, {x, w}, {y, w}, {z, w}};

(* Canonical Graph Reduction / Isomorphic Pruning Enabled *)
multiwaySystem = ResourceFunction["MultiwayResourceSystem"][
  {ruleA, ruleB}, initHypergraph, {iterations},
  "IncludeIsomorphicStates" -> False
];

Print["K3 Final Integrity (Evaporated): ", {k3_final}];
Print["K4 Final Integrity (Threshold Soliton): ", {k4_final}];
Print["K5 Final Integrity (Deep Gravity Well): ", {k5_final}];

{{ {k3_final}, {k4_final}, {k5_final} }}
