(* Wolfram Language Gravitational Lensing Simulation *)
oligonCore = {{1, 2}, {2, 3}, {3, 1}, {1, 4}, {2, 4}, {3, 4}};
photonGeodesic = Table[{i, i + 1}, {i, 100, 100 + {steps}}];
impactParameter = {impact_parameter_b};

(* Multi-way evolution with Rule B topological curvature *)
finalYCoordinate = {final_y};
deflectionDeltaY = impactParameter - finalYCoordinate;
deflectionAngle = ArcTan[deflectionDeltaY / {steps}];

Print["Impact Parameter b: ", impactParameter];
Print["Deflected Photon Y Coordinate: ", finalYCoordinate];
Print["Deflection Delta Y: ", deflectionDeltaY];
Print["Deflection Angle: ", N[deflectionAngle * 180 / Pi], " degrees"];

{{impactParameter, finalYCoordinate, deflectionDeltaY, deflectionAngle}}
