import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os
import torch

def generate_wolfram_hypergraph_visualization(output_path):
    print("Generating Wolfram-style Hypergraph Visualization...")
    
    # 1. Create a background 2D lattice (Vacuum)
    G = nx.grid_2d_graph(20, 20)
    
    # Remap nodes to integer IDs
    mapping = {node: i for i, node in enumerate(G.nodes())}
    G = nx.relabel_nodes(G, mapping)
    
    # 2. Inject a K4 "Oligon" Tangled Defect (Dark Matter)
    center_nodes = [190, 191, 210, 211, 189, 192, 209, 212]
    
    # Fully connect the core to simulate a high-density hypergraph tangle
    for i in range(len(center_nodes)):
        for j in range(i + 1, len(center_nodes)):
            G.add_edge(center_nodes[i], center_nodes[j])
            
    # Add some radiating connections (gravitational lensing/long-range threads)
    for n in center_nodes:
        for offset in [5, -5, 100, -100]:
            if n + offset in G.nodes():
                G.add_edge(n, n + offset)
                
    # 3. Compute layout
    # Use spring layout but fix the outer boundary to maintain the lattice shape
    pos = nx.spring_layout(G, k=0.15, iterations=50, seed=42)
    
    # 4. Compute curvature-like metric (Degree centrality as a proxy for visualization)
    degrees = dict(G.degree())
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        d = degrees[node]
        if d > 5:
            # Defect / Tangle (High curvature)
            node_colors.append('#ff0055') # Neon pink/red
            node_sizes.append(d * 10)
        else:
            # Vacuum (Flat)
            node_colors.append('#00aaff') # Neon blue
            node_sizes.append(10)
            
    # 5. Plotting (Dark Theme)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(14, 14), facecolor='#0b0f19')
    ax.set_facecolor('#0b0f19')
    
    # Draw edges with varying alpha based on connection to the defect
    edges = G.edges()
    edge_colors = []
    edge_alphas = []
    for u, v in edges:
        if degrees[u] > 5 or degrees[v] > 5:
            edge_colors.append('#ff0055')
            edge_alphas.append(0.6)
        else:
            edge_colors.append('#335577')
            edge_alphas.append(0.2)
            
    for i, edge in enumerate(edges):
        nx.draw_networkx_edges(G, pos, edgelist=[edge], width=1.5, alpha=edge_alphas[i], edge_color=edge_colors[i], ax=ax)
        
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.9, ax=ax, edgecolors='white', linewidths=0.5)
    
    # Aesthetics
    plt.title("Oligon K4 Topological Defect within Flat Vacuum Hypergraph", fontsize=24, color='white', fontfamily='monospace', pad=20)
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path, format='png', dpi=300, bbox_inches='tight', facecolor='#0b0f19')
    plt.close()
    print(f"Visualization saved successfully to {output_path}")

if __name__ == "__main__":
    os.makedirs("paper", exist_ok=True)
    generate_wolfram_hypergraph_visualization("paper/wolfram_hypergraph_visualization.png")
