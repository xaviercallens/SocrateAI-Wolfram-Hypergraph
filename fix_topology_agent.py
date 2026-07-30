import re

with open('agents/topology_agent/topology_agent.py', 'r') as f:
    content = f.read()

# Replace execute_multiway_oligon_poc
old_poc = """        r_curvature = v_tangle_hist[-1] / max(1, v_vacuum_hist[-1])
        
        wolfram_code = \"\"\"
(* Wolfram Language Multi-Way Causal Graph for Oligon K4 Tangle *)
k4Seed = {{1, 2}, {2, 3}, {3, 1}, {1, 4}, {2, 4}, {3, 4}};
vacuumCycle = Table[{i, Mod[i, 11] + 5}, {i, 5, 15}];
initHypergraph = Union[k4Seed, vacuumCycle, {{1, 5}, {4, 10}}];

ruleA = {{x_, y_}, {x_, z_}} :> {{x, w}, {y, w}, {z, w}};
ruleB = {{x_, y_}, {y_, z_}, {z_, x_}} :> {{x, y}, {y, z}, {z, x}, {x, w}, {y, w}, {z, w}};

multiwayEvolution = ResourceFunction["MultiwayResourceSystem"][
  {ruleA, ruleB}, initHypergraph, %d
];

vTangle = %d;
vVacuum = %d;
curvatureRatioR = N[vTangle / vVacuum];

Print["VTangle at step %d: ", vTangle];
Print["VVacuum at step %d: ", vVacuum];
Print["Curvature Ratio R = VTangle / VVacuum: ", curvatureRatioR];
\"\"\" % (iterations, v_tangle_hist[-1], v_vacuum_hist[-1], iterations, iterations)"""
new_poc = """        r_curvature = v_tangle_hist[-1] / max(1, v_vacuum_hist[-1])
        
        with open("mcp/scripts/multiway_oligon_poc.wl", "r") as f:
            wolfram_code = f.read().format(
                iterations=iterations,
                vTangle=v_tangle_hist[-1],
                vVacuum=v_vacuum_hist[-1]
            )
            
        wolfram_result = {"status": "unverified"}
        if self.evaluator.is_available:
            wolfram_result = {
                "status": "success",
                "code_executed": wolfram_code.strip(),
                "curvature_ratio_R": round(r_curvature, 4),
                "wolfram_output": self.evaluator.evaluate_expression(wolfram_code)
            }
        else:
            wolfram_result = {
                "status": "success_offline",
                "code_executed": wolfram_code.strip(),
                "curvature_ratio_R": round(r_curvature, 4)
            }
            
        lean_result = self.lean_verifier.verify("proofs/Lean4/Oligon_Topology.lean")"""
content = content.replace(old_poc, new_poc)
content = content.replace('"wolfram_mcp_output": {\n                "status": "success",\n                "code_executed": wolfram_code.strip(),\n                "curvature_ratio_R": round(r_curvature, 4)\n            }', '"wolfram_mcp_output": wolfram_result')
content = content.replace('"lean4_verification": {\n                "status": "verified",\n                "file": "proofs/Lean4/Oligon_Topology.lean",\n                "theorem": "curvature_ratio_greater_than_one"\n            }', '"lean4_verification": lean_result')

# ----------------- Twobody attraction -----------------
old_tb = """        initial_d = geodesic_distance_history[0]
        final_d = geodesic_distance_history[-1]
        delta_d = round(final_d - initial_d, 2)
        
        wolfram_code = f\"\"\"
(* Wolfram Language Multi-Way Two-Body K4 Oligon Attraction *)
k4Tangle1 = {{{{1, 2}}, {{2, 3}}, {{3, 1}}, {{1, 4}}, {{2, 4}}, {{3, 4}}}};
k4Tangle2 = {{{{25, 26}}, {{26, 27}}, {{27, 25}}, {{25, 28}}, {{26, 28}}, {{27, 28}}}};
vacuumCycle = Table[{{i, Mod[i - 5 + 1, 20] + 5}}, {{i, 5, 24}}];
couplings = {{{{4, 5}}, {{24, 25}}}};

initHypergraph = Union[k4Tangle1, k4Tangle2, vacuumCycle, couplings];

ruleA = {{{{x_, y_}}, {{x_, z_}}}} :> {{{{x, w}}, {{y, w}}, {{z, w}}}};
ruleB = {{{{x_, y_}}, {{y_, z_}}, {{z_, x_}}}} :> {{{{x, y}}, {{y, z}}, {{z, x}}, {{x, w}}, {{y, w}}, {{z, w}}}};

multiwayEvolution = ResourceFunction["MultiwayResourceSystem"][
  {{ruleA, ruleB}}, initHypergraph, {iterations}
];

initialDistance = {initial_d};
finalDistance = {final_d};
geodesicContraction = initialDistance - finalDistance;

Print["Initial Geodesic Distance d_0: ", initialDistance];
Print["Final Geodesic Distance d_7: ", finalDistance];
Print["Gravitational Attraction Delta d: ", geodesicContraction];
\"\"\""""
new_tb = """        initial_d = geodesic_distance_history[0]
        final_d = geodesic_distance_history[-1]
        delta_d = round(final_d - initial_d, 2)
        
        with open("mcp/scripts/twobody_attraction_poc.wl", "r") as f:
            wolfram_code = f.read().format(
                iterations=iterations,
                initial_d=initial_d,
                final_d=final_d
            )
            
        wolfram_result = {"status": "unverified"}
        if self.evaluator.is_available:
            wolfram_result = {
                "status": "success",
                "code_executed": wolfram_code.strip(),
                "initial_distance": initial_d,
                "final_distance": final_d,
                "contraction": abs(delta_d),
                "wolfram_output": self.evaluator.evaluate_expression(wolfram_code)
            }
        else:
            wolfram_result = {
                "status": "success_offline",
                "code_executed": wolfram_code.strip(),
                "initial_distance": initial_d,
                "final_distance": final_d,
                "contraction": abs(delta_d)
            }
            
        lean_result = self.lean_verifier.verify("proofs/Lean4/Oligon_Attraction.lean")"""
content = content.replace(old_tb, new_tb)
content = content.replace('"wolfram_mcp_output": {\n                "status": "success",\n                "code_executed": wolfram_code.strip(),\n                "initial_distance": initial_d,\n                "final_distance": final_d,\n                "contraction": abs(delta_d)\n            }', '"wolfram_mcp_output": wolfram_result')
content = content.replace('"lean4_verification": {\n                "status": "verified",\n                "file": "proofs/Lean4/Oligon_Attraction.lean",\n                "theorem": "two_body_geodesic_attraction"\n            }', '"lean4_verification": lean_result')

# ----------------- Gravitational lensing -----------------
old_gl = """        initial_y = photon_y_history[0]
        final_y = photon_y_history[-1]
        deflection_delta_y = round(initial_y - final_y, 2)
        
        # Deflection angle theta in radians / degrees
        import math
        deflection_angle_deg = round(math.degrees(math.atan2(deflection_delta_y, steps)), 2)
        
        wolfram_code = f\"\"\"
(* Wolfram Language Gravitational Lensing Simulation *)
oligonCore = {{{{1, 2}}, {{2, 3}}, {{3, 1}}, {{1, 4}}, {{2, 4}}, {{3, 4}}}};
photonGeodesic = Table[{{i, i + 1}}, {{i, 100, 100 + {steps}}}];
impactParameter = {impact_parameter_b};

(* Multi-way evolution with Rule B topological curvature *)
finalYCoordinate = {final_y};
deflectionDeltaY = impactParameter - finalYCoordinate;
deflectionAngle = ArcTan[deflectionDeltaY / {steps}];

Print["Impact Parameter b: ", impactParameter];
Print["Deflected Photon Y Coordinate: ", finalYCoordinate];
Print["Deflection Delta Y: ", deflectionDeltaY];
Print["Deflection Angle: ", N[deflectionAngle * 180 / Pi], " degrees"];
\"\"\""""
new_gl = """        initial_y = photon_y_history[0]
        final_y = photon_y_history[-1]
        deflection_delta_y = round(initial_y - final_y, 2)
        
        # Deflection angle theta in radians / degrees
        import math
        deflection_angle_deg = round(math.degrees(math.atan2(deflection_delta_y, steps)), 2)
        
        with open("mcp/scripts/gravitational_lensing_poc.wl", "r") as f:
            wolfram_code = f.read().format(
                steps=steps,
                impact_parameter_b=impact_parameter_b,
                final_y=final_y
            )
            
        wolfram_result = {"status": "unverified"}
        if self.evaluator.is_available:
            wolfram_result = {
                "status": "success",
                "code_executed": wolfram_code.strip(),
                "deflection_delta_y": deflection_delta_y,
                "deflection_angle_deg": deflection_angle_deg,
                "wolfram_output": self.evaluator.evaluate_expression(wolfram_code)
            }
        else:
            wolfram_result = {
                "status": "success_offline",
                "code_executed": wolfram_code.strip(),
                "deflection_delta_y": deflection_delta_y,
                "deflection_angle_deg": deflection_angle_deg
            }
            
        lean_result = self.lean_verifier.verify("proofs/Lean4/Gravitational_Lensing.lean")"""
content = content.replace(old_gl, new_gl)
content = content.replace('"wolfram_mcp_output": {\n                "status": "success",\n                "code_executed": wolfram_code.strip(),\n                "deflection_delta_y": deflection_delta_y,\n                "deflection_angle_deg": deflection_angle_deg\n            }', '"wolfram_mcp_output": wolfram_result')
content = content.replace('"lean4_verification": {\n                "status": "verified",\n                "file": "proofs/Lean4/Gravitational_Lensing.lean",\n                "theorem": "photon_path_bends_inward"\n            }', '"lean4_verification": lean_result')

# ----------------- MFDM Mass Spectrum Trial -----------------
old_ms = """            results[seed_name] = {
                "nodes": seed_data["nodes"],
                "initial_edges": seed_data["initial_edges"],
                "density_injection_rate": density_rate,
                "vacuum_expansion_rate": vacuum_expansion_rate_H,
                "final_bound_integrity": survival_history[-1],
                "integrity_history": survival_history,
                "status": status,
                "mfdm_mass_state": "SUB_THRESHOLD_DISPERSION" if not is_stable else ("THRESHOLD_STABLE_SOLITON" if seed_name == "K4" else "ULTRA_DENSE_CORE")
            }
            
        wolfram_code = f\"\"\"
(* Wolfram Language MFDM Mass Spectrum Trial *)
vacuumRate = {vacuum_expansion_rate_H};
k3Edges = 3; k4Edges = 6; k5Edges = 10;

k3Integrity = Table[k3Edges + (0.8 - vacuumRate) * t, {{t, 0, {iterations}}}];
k4Integrity = Table[k4Edges + (1.5 - vacuumRate) * t, {{t, 0, {iterations}}}];
k5Integrity = Table[k5Edges + (3.2 - vacuumRate) * t, {{t, 0, {iterations}}}];

Print["K3 Final Integrity: ", Last[k3Integrity], " -> Dissolved by Dark Energy"];
Print["K4 Final Integrity: ", Last[k4Integrity], " -> Stable MFDM Soliton Threshold"];
Print["K5 Final Integrity: ", Last[k5Integrity], " -> Ultra-Dense Core"];
\"\"\""""
new_ms = """            results[seed_name] = {
                "nodes": seed_data["nodes"],
                "initial_edges": seed_data["initial_edges"],
                "density_injection_rate": density_rate,
                "vacuum_expansion_rate": vacuum_expansion_rate_H,
                "final_bound_integrity": survival_history[-1],
                "integrity_history": survival_history,
                "status": status,
                "mfdm_mass_state": "SUB_THRESHOLD_DISPERSION" if not is_stable else ("THRESHOLD_STABLE_SOLITON" if seed_name == "K4" else "ULTRA_DENSE_CORE")
            }
            
        with open("mcp/scripts/mfdm_mass_spectrum_trial.wl", "r") as f:
            wolfram_code = f.read().format(
                vacuum_expansion_rate_H=vacuum_expansion_rate_H,
                iterations=iterations
            )
            
        wolfram_result = {"status": "unverified"}
        if self.evaluator.is_available:
            wolfram_result = {
                "status": "success",
                "code_executed": wolfram_code.strip(),
                "k3_final": results["K3"]["final_bound_integrity"],
                "k4_final": results["K4"]["final_bound_integrity"],
                "k5_final": results["K5"]["final_bound_integrity"],
                "wolfram_output": self.evaluator.evaluate_expression(wolfram_code)
            }
        else:
            wolfram_result = {
                "status": "success_offline",
                "code_executed": wolfram_code.strip(),
                "k3_final": results["K3"]["final_bound_integrity"],
                "k4_final": results["K4"]["final_bound_integrity"],
                "k5_final": results["K5"]["final_bound_integrity"]
            }
            
        lean_result = self.lean_verifier.verify("proofs/Lean4/MFDM_Mass_Spectrum.lean")"""
content = content.replace(old_ms, new_ms)
content = content.replace('"wolfram_mcp_output": {\n                "status": "success",\n                "code_executed": wolfram_code.strip(),\n                "k3_final": results["K3"]["final_bound_integrity"],\n                "k4_final": results["K4"]["final_bound_integrity"],\n                "k5_final": results["K5"]["final_bound_integrity"]\n            }', '"wolfram_mcp_output": wolfram_result')
content = content.replace('"lean4_verification": {\n                "status": "verified",\n                "file": "proofs/Lean4/MFDM_Mass_Spectrum.lean",\n                "theorem": "k3_dissolves_under_expansion"\n            }', '"lean4_verification": lean_result')


# ----------------- Simultaneous K3 K5 -----------------
old_sk = """        k5_gravity_well_curvature = round(k5_integrity_hist[-1] / max(1.0, k3_integrity_hist[-1] + 1.0), 2)
        
        wolfram_code = f\"\"\"
(* Wolfram Language Simultaneous K3 vs K5 Mass Spectrum Trial *)
k3Seed = {{{{1, 2}}, {{2, 3}}, {{3, 1}}}};
k5Seed = {{{{20, 21}}, {{21, 22}}, {{22, 23}}, {{23, 24}}, {{24, 20}}, {{20, 22}}, {{21, 23}}, {{22, 24}}, {{23, 20}}, {{24, 21}}}};
vacuumBridge = Table[{{i, Mod[i - 4 + 1, 16] + 4}}, {{i, 4, 19}}];

initHypergraph = Union[k3Seed, k5Seed, vacuumBridge];

k3FinalIntegrity = {k3_integrity_hist[-1]};
k5FinalIntegrity = {k5_integrity_hist[-1]};
k5CurvatureRatio = {k5_gravity_well_curvature};

Print["K3 Final Integrity (Evaporated): ", k3FinalIntegrity];
Print["K5 Final Integrity (Deep Gravity Well): ", k5FinalIntegrity];
Print["K5 Curvature Ratio R: ", k5CurvatureRatio];
\"\"\""""
new_sk = """        k5_gravity_well_curvature = round(k5_integrity_hist[-1] / max(1.0, k3_integrity_hist[-1] + 1.0), 2)
        
        with open("mcp/scripts/simultaneous_k3_k5.wl", "r") as f:
            wolfram_code = f.read().format(
                k3_final=k3_integrity_hist[-1],
                k5_final=k5_integrity_hist[-1],
                k5_curvature=k5_gravity_well_curvature
            )
            
        wolfram_result = {"status": "unverified"}
        if self.evaluator.is_available:
            wolfram_result = {
                "status": "success",
                "code_executed": wolfram_code.strip(),
                "k3_final": k3_integrity_hist[-1],
                "k5_final": k5_integrity_hist[-1],
                "k5_curvature_ratio": k5_gravity_well_curvature,
                "wolfram_output": self.evaluator.evaluate_expression(wolfram_code)
            }
        else:
            wolfram_result = {
                "status": "success_offline",
                "code_executed": wolfram_code.strip(),
                "k3_final": k3_integrity_hist[-1],
                "k5_final": k5_integrity_hist[-1],
                "k5_curvature_ratio": k5_gravity_well_curvature
            }
            
        lean_result = self.lean_verifier.verify("proofs/Lean4/Simultaneous_Mass_Trial.lean")"""
content = content.replace(old_sk, new_sk)
content = content.replace('"wolfram_mcp_output": {\n                "status": "success",\n                "code_executed": wolfram_code.strip(),\n                "k3_final": k3_integrity_hist[-1],\n                "k5_final": k5_integrity_hist[-1],\n                "k5_curvature_ratio": k5_gravity_well_curvature\n            }', '"wolfram_mcp_output": wolfram_result')
content = content.replace('"lean4_verification": {\n                "status": "verified",\n                "file": "proofs/Lean4/Simultaneous_Mass_Trial.lean",\n                "theorem": "k3_evaporates_and_k5_forms_gravity_well"\n            }', '"lean4_verification": lean_result')

# ----------------- K3/K4/K5 Pruned -----------------
old_kp = """            k5_hist.append(float(len(k5_engine.edges)))
            
        wolfram_code = f\"\"\"
(* Wolfram Language Simultaneous K3/K4/K5 Mass Spectrum Trial with Isomorphic Pruning *)
k3Seed = {{{{1, 2}}, {{2, 3}}, {{3, 1}}}};
k4Seed = {{{{10, 11}}, {{11, 12}}, {{12, 10}}, {{10, 13}}, {{11, 13}}, {{12, 13}}}};
k5Seed = {{{{20, 21}}, {{21, 22}}, {{22, 23}}, {{23, 24}}, {{24, 20}}, {{20, 22}}, {{21, 23}}, {{22, 24}}, {{23, 20}}, {{24, 21}}}};

initHypergraph = Union[k3Seed, k4Seed, k5Seed];

ruleA = {{{{x_, y_}}, {{x_, z_}}}} :> {{{{x, w}}, {{y, w}}, {{z, w}}}};
ruleB = {{{{x_, y_}}, {{y_, z_}}, {{z_, x_}}}} :> {{{{x, y}}, {{y, z}}, {{z, x}}, {{x, w}}, {{y, w}}, {{z, w}}}};

(* Canonical Graph Reduction / Isomorphic Pruning Enabled *)
multiwaySystem = ResourceFunction["MultiwayResourceSystem"][
  {{ruleA, ruleB}}, initHypergraph, {iterations},
  "IncludeIsomorphicStates" -> False
];

Print["K3 Final Integrity (Evaporated): ", {k3_hist[-1]}];
Print["K4 Final Integrity (Threshold Soliton): ", {k4_hist[-1]}];
Print["K5 Final Integrity (Deep Gravity Well): ", {k5_hist[-1]}];
\"\"\""""
new_kp = """            k5_hist.append(float(len(k5_engine.edges)))
            
        with open("mcp/scripts/k3_k4_k5_pruned.wl", "r") as f:
            wolfram_code = f.read().format(
                iterations=iterations,
                k3_final=k3_hist[-1],
                k4_final=k4_hist[-1],
                k5_final=k5_hist[-1]
            )
            
        wolfram_result = {"status": "unverified"}
        if self.evaluator.is_available:
            wolfram_result = {
                "status": "success",
                "code_executed": wolfram_code.strip(),
                "k3_final": k3_hist[-1],
                "k4_final": k4_hist[-1],
                "k5_final": k5_hist[-1],
                "wolfram_output": self.evaluator.evaluate_expression(wolfram_code)
            }
        else:
            wolfram_result = {
                "status": "success_offline",
                "code_executed": wolfram_code.strip(),
                "k3_final": k3_hist[-1],
                "k4_final": k4_hist[-1],
                "k5_final": k5_hist[-1]
            }
            
        lean_result = self.lean_verifier.verify("proofs/Lean4/K3_K4_K5_Pruned_Spectrum.lean")"""
content = content.replace(old_kp, new_kp)
content = content.replace('"wolfram_mcp_output": {\n                "status": "success",\n                "code_executed": wolfram_code.strip(),\n                "k3_final": k3_hist[-1],\n                "k4_final": k4_hist[-1],\n                "k5_final": k5_hist[-1]\n            }', '"wolfram_mcp_output": wolfram_result')
content = content.replace('"lean4_verification": {\n                "status": "verified",\n                "file": "proofs/Lean4/K3_K4_K5_Pruned_Spectrum.lean",\n                "theorem": "k3_evaporates_k4_stable_k5_gravity_well"\n            }', '"lean4_verification": lean_result')

with open('agents/topology_agent/topology_agent.py', 'w') as f:
    f.write(content)
