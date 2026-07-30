"""
Topological Data Analysis (TDA) for Dual-Scale K3xT2 Validation
Extracts Discrete Ricci Curvature and Euler Characteristic from Hypergraph Checkpoints.
"""

import torch
import networkx as nx
import numpy as np
import json
import time
import os
import sys

try:
    from GraphRicciCurvature.FormanRicci import FormanRicci
except ImportError:
    print("CRITICAL: Please install GraphRicciCurvature -> `pip install GraphRicciCurvature`")
    exit(1)

def load_checkpoint_to_graph(checkpoint_path: str) -> nx.Graph:
    """Loads a PyTorch sparse tensor checkpoint into a NetworkX graph."""
    print(f"[TDA] Loading checkpoint from {checkpoint_path}...")
    try:
        checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'), weights_only=False)
    except Exception:
        checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))
    
    # Handle different checkpoint formats (dict vs raw tensor vs point cloud)
    if isinstance(checkpoint, dict) and 'ra' in checkpoint and 'dec' in checkpoint and 'z' in checkpoint:
        from scipy.spatial import KDTree
        ra = np.asarray(checkpoint['ra'])
        dec = np.asarray(checkpoint['dec'])
        redshift = np.asarray(checkpoint['z'])
        # Convert ra, dec, z to 3D Cartesian coordinates
        r = redshift + 1.0  # approximate distance proxy
        dec_rad = np.radians(dec)
        ra_rad = np.radians(ra)
        x = r * np.cos(dec_rad) * np.cos(ra_rad)
        y = r * np.cos(dec_rad) * np.sin(ra_rad)
        z_coord = r * np.sin(dec_rad)
        points = np.column_stack([x, y, z_coord])
        
        # Subsample if nodes > 10,000 for local T4 feasibility
        if len(points) > 10000:
            np.random.seed(42)
            idx = np.random.choice(len(points), 10000, replace=False)
            points = points[idx]
            
        tree = KDTree(points)
        # k=6 nearest neighbors graph
        k = 6
        distances, indices = tree.query(points, k=k)
        G = nx.Graph()
        for i in range(len(points)):
            for neighbor_idx in indices[i, 1:]:
                G.add_edge(int(i), int(neighbor_idx))
        print(f"[TDA] Point cloud graph constructed from RA, DEC, Z. Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
        return G
    elif isinstance(checkpoint, dict) and 'adjacency_matrix' in checkpoint:
        M_t = checkpoint['adjacency_matrix']
    elif isinstance(checkpoint, dict) and 'state_matrix' in checkpoint:
        M_t = checkpoint['state_matrix']
    else:
        M_t = checkpoint
        
    if hasattr(M_t, "is_sparse") and M_t.is_sparse:
        # Convert sparse tensor to scipy sparse matrix, then to NetworkX
        indices = M_t.indices().numpy()
        edges = [(int(indices[0, i]), int(indices[1, i])) for i in range(indices.shape[1])]
        G = nx.Graph()
        G.add_edges_from(edges)
    elif hasattr(M_t, "to_dense"):
        M_dense = M_t.to_dense().numpy()
        G = nx.from_numpy_array(M_dense)
    elif isinstance(M_t, torch.Tensor):
        G = nx.from_numpy_array(M_t.numpy())
    elif isinstance(M_t, np.ndarray):
        G = nx.from_numpy_array(M_t)
    else:
        raise ValueError(f"Unrecognized matrix type: {type(M_t)}")
        
    print(f"[TDA] Graph loaded. Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
    return G

def extract_euler_characteristic(G_subgraph: nx.Graph) -> int:
    """
    Computes the Euler Characteristic (chi = V - E + F - T) for a localized subgraph.
    V = Vertices, E = Edges, F = Faces (Triangles), T = Tetrahedra (4-cliques)
    """
    print("[TDA] Computing simplicial complexes for Euler Characteristic...")
    
    V = G_subgraph.number_of_nodes()
    E = G_subgraph.number_of_edges()
    
    # Find all cliques to count faces and tetrahedra
    cliques = list(nx.find_cliques(G_subgraph))
    
    F = sum(1 for c in cliques if len(c) == 3)
    T = sum(1 for c in cliques if len(c) == 4)
    
    # Higher dimensional simplices (if any exist in the tangle)
    S5 = sum(1 for c in cliques if len(c) == 5)
    
    chi = V - E + F - T + S5
    print(f"[TDA] Localized Topology -> V:{V}, E:{E}, F:{F}, T:{T}, S5:{S5}")
    print(f"[TDA] Euler Characteristic (chi) = {chi}")
    
    return chi

def validate_k3_geometry(checkpoint_path: str, output_json: str):
    """Main execution pipeline to validate K3 surface signatures."""
    start_time = time.time()
    
    # 1. Load Graph
    G = load_checkpoint_to_graph(checkpoint_path)
    
    # 2. Compute Forman-Ricci Curvature
    print("[TDA] Computing Forman-Ricci Curvature across the manifold...")
    frc = FormanRicci(G, method="1d", verbose="INFO")
    frc.compute_ricci_curvature()
    
    # Extract curvatures
    edge_curvatures = [data['formanCurvature'] for _, _, data in frc.G.edges(data=True)]
    node_curvatures = [data['formanCurvature'] for _, data in frc.G.nodes(data=True)]
    
    # 3. Analyze Vacuum vs. Defect Curvature
    # A Calabi-Yau manifold (K3) must be Ricci-flat in the vacuum (curvature ~ 0)
    vacuum_nodes = [n for n in node_curvatures if abs(n) < 0.1]
    defect_nodes = [n for n in node_curvatures if abs(n) >= 0.1]
    
    ricci_flatness_ratio = len(vacuum_nodes) / max(1, len(node_curvatures))
    print(f"[TDA] Ricci-Flatness (Vacuum Ratio): {ricci_flatness_ratio * 100:.2f}% of space is flat.")
    
    # 4. Localized Euler Characteristic on the Core Anomaly
    # Extract the subgraph of highly curved nodes (The merged Dark Matter Halo)
    core_nodes = [n for n, data in frc.G.nodes(data=True) if data['formanCurvature'] < -2.0 or data['formanCurvature'] > 2.0]
    
    if not core_nodes:
        print("[TDA] No highly curved core detected. Euler characteristic extraction fallback to core connected component / high-degree nodes.")
        core_nodes = [n for n, d in G.degree() if d >= 3]
        if not core_nodes:
            core_nodes = list(G.nodes())
        
    G_core = G.subgraph(core_nodes)
    chi = extract_euler_characteristic(G_core)
        
    # 5. Export Results
    results = {
        "metrics": {
            "checkpoint": checkpoint_path,
            "total_nodes": G.number_of_nodes(),
            "total_edges": G.number_of_edges(),
            "ricci_flatness_ratio": float(ricci_flatness_ratio),
            "max_positive_curvature": float(max(node_curvatures)) if node_curvatures else 0.0,
            "max_negative_curvature": float(min(node_curvatures)) if node_curvatures else 0.0,
            "core_euler_characteristic_chi": chi,
            "k3_surface_signature_detected": bool(chi == 24 or (chi != 0 and chi % 24 == 0))
        }
    }
    
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2)
        
    print(f"\n[TDA] Geometric Validation Complete in {time.time() - start_time:.2f} seconds.")
    print(f"[TDA] Results saved to {output_json}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        CHECKPOINT_FILE = sys.argv[1]
    else:
        default_path = "/mnt/disks/disk-socrateai-local-1/hypergraph_logs/batch_runs/checkpoint_step_100000.pt"
        if os.path.exists(default_path):
            CHECKPOINT_FILE = default_path
        else:
            import glob
            files = sorted(glob.glob("/mnt/disks/disk-socrateai-local-1/hypergraph_logs/batch_runs/checkpoint_step_*.pt"), key=os.path.getmtime, reverse=True)
            if files:
                CHECKPOINT_FILE = files[0]
            else:
                CHECKPOINT_FILE = default_path

    OUTPUT_FILE = "k3_geometric_validation.json"
    
    validate_k3_geometry(CHECKPOINT_FILE, OUTPUT_FILE)
