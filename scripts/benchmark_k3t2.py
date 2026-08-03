import time
import random
import tracemalloc

ATOMS_PER_SEC = 10

# ---------------------------------------------------------------------------
# RUN 1: Baseline (Full Re-computation per frame)
# ---------------------------------------------------------------------------
class BaselineEngine:
    def __init__(self):
        self.baseK3T2 = None

    def get_base_topology(self):
        if self.baseK3T2:
            return self.baseK3T2
        
        nodes = []
        edges = []
        k3_nodes = 24
        k3_edges = []
        for i in range(k3_nodes):
            k3_edges.append([i, (i + 1) % k3_nodes])
            k3_edges.append([i, (i + 2) % k3_nodes])
            k3_edges.append([i, (i + 3) % k3_nodes])
            
        t2_dim = 4
        t2_nodes = t2_dim * t2_dim
        t2_edges = []
        for r in range(t2_dim):
            for c in range(t2_dim):
                u = r * t2_dim + c
                down = ((r + 1) % t2_dim) * t2_dim + c
                right = r * t2_dim + ((c + 1) % t2_dim)
                t2_edges.append([u, down])
                t2_edges.append([u, right])
                
        for u in range(k3_nodes):
            for v in range(t2_nodes):
                id_val = u * t2_nodes + v
                nodes.append({"id": str(id_val), "type": "k3" if u % 2 == 0 else "t2"})
                
        for u in range(k3_nodes):
            for v in range(t2_nodes):
                id_val = u * t2_nodes + v
                for v1, v2 in t2_edges:
                    if v == v1:
                        edges.append({"source": str(id_val), "target": str(u * t2_nodes + v2)})
                for u1, u2 in k3_edges:
                    if u == u1:
                        edges.append({"source": str(id_val), "target": str(u2 * t2_nodes + v)})
                        
        self.baseK3T2 = {"nodes": nodes, "edges": edges}
        return self.baseK3T2

    def generate_frame(self, frame_index):
        base = self.get_base_topology()
        nodes = list(base["nodes"])
        edges = list(base["edges"])
        
        extra_nodes = frame_index * ATOMS_PER_SEC
        base_count = len(nodes)
        
        for i in range(extra_nodes):
            new_id = str(base_count + i)
            nodes.append({"id": new_id, "type": "vacuum"})
            target1 = str(random.randint(0, base_count + i - 1))
            edges.append({"source": new_id, "target": target1})
            if i % 2 == 0:
                target2 = str(random.randint(0, base_count + i - 1))
                edges.append({"source": new_id, "target": target2})
                
        return {"nodes": nodes, "edges": edges}


# ---------------------------------------------------------------------------
# RUN 2: Incremental Accumulation Engine (Reuse previous frame state)
# ---------------------------------------------------------------------------
class IncrementalEngine(BaselineEngine):
    def __init__(self):
        super().__init__()
        self.current_nodes = []
        self.current_edges = []
        self.node_count = 0

    def init_sequence(self):
        base = self.get_base_topology()
        self.current_nodes = list(base["nodes"])
        self.current_edges = list(base["edges"])
        self.node_count = len(self.current_nodes)

    def advance_frame(self):
        # Add only 10 nodes per frame step instead of recalculating from zero
        for i in range(ATOMS_PER_SEC):
            new_id = str(self.node_count)
            self.current_nodes.append({"id": new_id, "type": "vacuum"})
            target1 = str(random.randint(0, self.node_count - 1))
            self.current_edges.append({"source": new_id, "target": target1})
            if i % 2 == 0:
                target2 = str(random.randint(0, self.node_count - 1))
                self.current_edges.append({"source": new_id, "target": target2})
            self.node_count += 1
            
        return {"nodes": self.current_nodes, "edges": self.current_edges}


# ---------------------------------------------------------------------------
# RUN 3: Fast Cached String & Pre-allocated ID Engine (Maximum Performance)
# ---------------------------------------------------------------------------
class OptimizedCachedEngine:
    def __init__(self):
        self.base_nodes = []
        self.base_edges = []
        self.id_str_cache = [str(i) for i in range(10000)]
        self.current_nodes = []
        self.current_edges = []
        self.node_count = 0

    def init_sequence(self):
        # Pre-compute with cached string references
        k3_nodes = 24
        k3_edges = []
        for i in range(k3_nodes):
            k3_edges.append([i, (i + 1) % k3_nodes])
            k3_edges.append([i, (i + 2) % k3_nodes])
            k3_edges.append([i, (i + 3) % k3_nodes])
        
        t2_dim = 4
        t2_nodes = t2_dim * t2_dim
        t2_edges = []
        for r in range(t2_dim):
            for c in range(t2_dim):
                u = r * t2_dim + c
                down = ((r + 1) % t2_dim) * t2_dim + c
                right = r * t2_dim + ((c + 1) % t2_dim)
                t2_edges.append([u, down])
                t2_edges.append([u, right])
                
        self.current_nodes = []
        self.current_edges = []
        
        for u in range(k3_nodes):
            for v in range(t2_nodes):
                id_val = u * t2_nodes + v
                self.current_nodes.append({"id": self.id_str_cache[id_val], "type": "k3" if u % 2 == 0 else "t2"})
                
        for u in range(k3_nodes):
            for v in range(t2_nodes):
                id_val = u * t2_nodes + v
                for v1, v2 in t2_edges:
                    if v == v1:
                        self.current_edges.append({"source": self.id_str_cache[id_val], "target": self.id_str_cache[u * t2_nodes + v2]})
                for u1, u2 in k3_edges:
                    if u == u1:
                        self.current_edges.append({"source": self.id_str_cache[id_val], "target": self.id_str_cache[u2 * t2_nodes + v]})
                        
        self.node_count = len(self.current_nodes)

    def advance_frame(self):
        for i in range(ATOMS_PER_SEC):
            new_id_str = self.id_str_cache[self.node_count] if self.node_count < 10000 else str(self.node_count)
            self.current_nodes.append({"id": new_id_str, "type": "vacuum"})
            
            t1 = random.randint(0, self.node_count - 1)
            t1_str = self.id_str_cache[t1] if t1 < 10000 else str(t1)
            self.current_edges.append({"source": new_id_str, "target": t1_str})
            
            if i % 2 == 0:
                t2 = random.randint(0, self.node_count - 1)
                t2_str = self.id_str_cache[t2] if t2 < 10000 else str(t2)
                self.current_edges.append({"source": new_id_str, "target": t2_str})
                
            self.node_count += 1
            
        return {"nodes": self.current_nodes, "edges": self.current_edges}


# ---------------------------------------------------------------------------
# Benchmark Suite Execution
# ---------------------------------------------------------------------------
def run_comparison():
    print("=========================================================")
    print("🚀 K3×T² PHYSICS ENGINE MULTI-RUN BENCHMARK COMPARISON")
    print("=========================================================\n")

    # ----- RUN 1 -----
    print("--- RUN 1: Baseline Engine (Full Re-computation per Frame) ---")
    tracemalloc.start()
    r1 = BaselineEngine()
    start_r1 = time.perf_counter()
    for i in range(1, 661):
        r1.generate_frame(i)
    end_r1 = time.perf_counter()
    time_r1 = (end_r1 - start_r1) * 1000
    _, peak_r1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"Total Sequence Time: {time_r1:.2f} ms ({time_r1/1000:.2f} s)")
    print(f"Avg Time per Frame:  {time_r1/660:.3f} ms")
    print(f"Peak Memory:         {peak_r1 / 1024 / 1024:.2f} MB\n")

    # ----- RUN 2 -----
    print("--- RUN 2: Incremental Accumulator Engine (O(N) Incremental) ---")
    tracemalloc.start()
    r2 = IncrementalEngine()
    start_r2 = time.perf_counter()
    r2.init_sequence()
    for i in range(1, 661):
        r2.advance_frame()
    end_r2 = time.perf_counter()
    time_r2 = (end_r2 - start_r2) * 1000
    _, peak_r2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    speedup_r2 = time_r1 / time_r2
    print(f"Total Sequence Time: {time_r2:.2f} ms ({time_r2/1000:.3f} s)")
    print(f"Avg Time per Frame:  {time_r2/660:.3f} ms")
    print(f"Peak Memory:         {peak_r2 / 1024 / 1024:.2f} MB")
    print(f"Speedup vs Run 1:    {speedup_r2:.2f}x faster 🚀\n")

    # ----- RUN 3 -----
    print("--- RUN 3: Fast Cached String & Pre-allocated ID Engine ---")
    tracemalloc.start()
    r3 = OptimizedCachedEngine()
    start_r3 = time.perf_counter()
    r3.init_sequence()
    for i in range(1, 661):
        r3.advance_frame()
    end_r3 = time.perf_counter()
    time_r3 = (end_r3 - start_r3) * 1000
    _, peak_r3 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    speedup_r3 = time_r1 / time_r3
    print(f"Total Sequence Time: {time_r3:.2f} ms ({time_r3/1000:.3f} s)")
    print(f"Avg Time per Frame:  {time_r3/660:.3f} ms")
    print(f"Peak Memory:         {peak_r3 / 1024 / 1024:.2f} MB")
    print(f"Speedup vs Run 1:    {speedup_r3:.2f}x faster 🚀 🔥\n")

    print("=========================================================")
    print("SUMMARY OF IMPROVEMENTS")
    print("=========================================================")
    print(f"Run 1 (Baseline):             {time_r1/660:.3f} ms/frame")
    print(f"Run 2 (Incremental):          {time_r2/660:.3f} ms/frame ({speedup_r2:.1f}x speedup)")
    print(f"Run 3 (Incremental + Cache): {time_r3/660:.3f} ms/frame ({speedup_r3:.1f}x speedup)")
    print("=========================================================")

if __name__ == "__main__":
    run_comparison()
