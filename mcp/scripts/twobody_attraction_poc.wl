(* Wolfram Language Multi-Way Two-Body K4 Oligon Attraction *)
k4Tangle1 = {{1, 2}, {2, 3}, {3, 1}, {1, 4}, {2, 4}, {3, 4}};
k4Tangle2 = {{25, 26}, {26, 27}, {27, 25}, {25, 28}, {26, 28}, {27, 28}};
vacuumCycle = Table[{i, Mod[i - 5 + 1, 20] + 5}, {i, 5, 24}];
couplings = {{4, 5}, {24, 25}};

initHypergraph = Union[k4Tangle1, k4Tangle2, vacuumCycle, couplings];

ruleA = {{x_, y_}, {x_, z_}} :> {{x, w}, {y, w}, {z, w}};
ruleB = {{x_, y_}, {y_, z_}, {z_, x_}} :> {{x, y}, {y, z}, {z, x}, {x, w}, {y, w}, {z, w}};

multiwayEvolution = ResourceFunction["MultiwayResourceSystem"][
  {ruleA, ruleB}, initHypergraph, {iterations}
];

initialDistance = {initial_d};
finalDistance = {final_d};
geodesicContraction = initialDistance - finalDistance;

Print["Initial Geodesic Distance d_0: ", initialDistance];
Print["Final Geodesic Distance d_7: ", finalDistance];
Print["Gravitational Attraction Delta d: ", geodesicContraction];

{{initialDistance, finalDistance, geodesicContraction}}
