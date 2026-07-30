(* Wolfram Language Multi-Way Causal Graph for Oligon K4 Tangle *)
k4Seed = {{1, 2}, {2, 3}, {3, 1}, {1, 4}, {2, 4}, {3, 4}};
vacuumCycle = Table[{i, Mod[i, 11] + 5}, {i, 5, 15}];
initHypergraph = Union[k4Seed, vacuumCycle, {{1, 5}, {4, 10}}];

ruleA = {{x_, y_}, {x_, z_}} :> {{x, w}, {y, w}, {z, w}};
ruleB = {{x_, y_}, {y_, z_}, {z_, x_}} :> {{x, y}, {y, z}, {z, x}, {x, w}, {y, w}, {z, w}};

multiwayEvolution = ResourceFunction["MultiwayResourceSystem"][
  {ruleA, ruleB}, initHypergraph, {iterations}
];

vTangle = {vTangle};
vVacuum = {vVacuum};
curvatureRatioR = N[vTangle / vVacuum];

Print["VTangle at step {iterations}: ", vTangle];
Print["VVacuum at step {iterations}: ", vVacuum];
Print["Curvature Ratio R = VTangle / VVacuum: ", curvatureRatioR];

{{vTangle, vVacuum, curvatureRatioR}}
