#!/usr/bin/env python3
"""
Google Antigravity JSON Topology Exporter (v4.0 GPU Pipeline)
=============================================================
Replaces the legacy CPU/Matplotlib renderer. This script now pre-computes 
the mathematical topology graphs for the K3xT2 simulation and dumps them
into a single JSON file for the Cosmograph WebGL frontend to render.
"""

import os
import json
import networkx as nx
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
OUT_DIR = os.path.join(WORKSPACE, "dashboard", "baked_outputs")
os.makedirs(OUT_DIR, exist_ok=True)

def generate_k3_t2_fiber_bundle(extra_nodes=0):
    """Generates K3 x T2 fiber bundle with dynamic node growth"""
    base_k3 = nx.circulant_graph(24, [1, 2, 3])
    fiber_t2 = nx.grid_graph(dim=[4, 4], periodic=True)
    fiber_t2 = nx.convert_node_labels_to_integers(fiber_t2)
    bundle = nx.cartesian_product(base_k3, fiber_t2)
    bundle = nx.convert_node_labels_to_integers(bundle)
    
    if extra_nodes > 0:
        num_existing = bundle.number_of_nodes()
        for i in range(extra_nodes):
            new_id = num_existing + i
            target = i % num_existing
            bundle.add_node(new_id)
            bundle.add_edge(new_id, target)
            bundle.add_edge(new_id, (target + 1) % num_existing)
            
    return bundle

def main():
    logging.info("🚀 Generating JSON Topology for 11-Minute Cosmograph Visualization...")
    
    frames = []
    # Just generate 5 keyframes to prevent massive file sizes. 
    # The frontend Cosmograph instance will interpolate the rest or generate on the fly.
    keyframes = [0, 100, 300, 500, 660]
    
    for f in keyframes:
        logging.info(f"Generating topology for frame {f} (+{f*10} atoms)")
        G = generate_k3_t2_fiber_bundle(extra_nodes=f * 10)
        
        nodes = [{"id": str(n)} for n in G.nodes()]
        edges = [{"source": str(u), "target": str(v)} for u, v in G.edges()]
        
        frames.append({
            "frame": f,
            "nodes": nodes,
            "edges": edges
        })
        
    out_file = os.path.join(OUT_DIR, "k3_t2_topology_keyframes.json")
    with open(out_file, "w") as f:
        json.dump(frames, f)
        
    logging.info(f"✅ Pre-computation complete. Data written to {out_file}.")
    logging.info(f"The Cosmograph frontend will now use this topology for GPU rendering.")

if __name__ == "__main__":
    main()
