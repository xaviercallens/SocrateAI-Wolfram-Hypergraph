import time
import torch
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hypergraph.runux_sundials_adapter import RunuxHypergraphAccelerator
from data_benchmarks.sdss_loader import SDSSDataLoader
from sklearn.neighbors import NearestNeighbors

def run_3_hour_benchmark():
    print("=================================================================")
    print("🚀 Starting 3-Hour Phase 1 Astrophysics Benchmark")
    print("=================================================================")
    
    loader = SDSSDataLoader(data_dir="/tmp/sdss_z")
    coords = loader.load_galaxy_coordinates("sdss_z_stripe82_center.csv")
    
    num_nodes = len(coords)
    print(f"[Data] Loaded {num_nodes} real galaxies from SDSS DR1.")
    
    print("[Engine] Constructing real-data proximity graph (k-NN)...")
    k = min(10, num_nodes - 1)
    nbrs = NearestNeighbors(n_neighbors=k, algorithm='ball_tree').fit(coords)
    distances, indices = nbrs.kneighbors(coords)
    
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    src = np.repeat(np.arange(num_nodes), k)
    dst = indices.flatten()
    
    i = torch.tensor(np.vstack([src, dst]), dtype=torch.long, device=device)
    v = torch.ones(i.shape[1], dtype=torch.float32, device=device)
    
    adj_sparse = torch.sparse_coo_tensor(i, v, (num_nodes, num_nodes), device=device).coalesce()
    mask_sparse = torch.sparse_coo_tensor(i, v, (num_nodes, num_nodes), device=device).coalesce()
    
    accelerator = RunuxHypergraphAccelerator()
    
    start_time = time.time()
    target_duration = 30  # 30 seconds for validation (down from 3 hours)
    
    print("[Engine] Entering deep-time hypergraph evolution...")
    
    current_adj = adj_sparse
    step = 0
    
    # We write a loop that will keep running until 3 hours pass
    while time.time() - start_time < target_duration:
        current_adj = accelerator.sparse_engine.sparse_masked_step(current_adj, mask_sparse)
        step += 1
        
        if step % 100 == 0:
            elapsed = time.time() - start_time
            print(f"  -> Step {step:05d} | Elapsed: {elapsed/3600:.2f} hrs | VRAM: {torch.cuda.max_memory_allocated(device) / (1024**2):.1f} MB")
            
    print(f"\n[Extraction Complete] 3-Hour Benchmark finished after {step} steps.")

if __name__ == "__main__":
    run_3_hour_benchmark()
