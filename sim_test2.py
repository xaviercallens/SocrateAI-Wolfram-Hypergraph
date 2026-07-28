class PurePythonHypergraphEngine:
    def __init__(self, edges):
        self.edges = set(tuple(sorted(e)) for e in edges)
        self.nodes = set(n for e in edges for n in e)
        self.next_node = max(self.nodes) + 1 if self.nodes else 1

    def step(self):
        adj = {n: set() for n in self.nodes}
        for u, v in self.edges:
            adj[u].add(v)
            adj[v].add(u)
            
        triangles = set()
        for x in self.nodes:
            for y in adj[x]:
                if y > x:
                    for z in adj[y]:
                        if z > y and z in adj[x]:
                            triangles.add(tuple(sorted((x, y, z))))
                            
        edge_triangle_count = {e: 0 for e in self.edges}
        for t in triangles:
            edge_triangle_count[tuple(sorted((t[0], t[1])))] += 1
            edge_triangle_count[tuple(sorted((t[1], t[2])))] += 1
            edge_triangle_count[tuple(sorted((t[0], t[2])))] += 1

        new_edges = set(self.edges)
        
        edges_to_remove = set()
        for e in self.edges:
            if edge_triangle_count[e] < 2:
                edges_to_remove.add(e)
                
        # Only add a limited number of new nodes to avoid exponential blowup causing OOM/slowness
        # We can add 1 node per K4 structure
        # A K4 is a set of 4 nodes where all 6 edges exist.
        k4s = set()
        for x in self.nodes:
            for y in adj[x]:
                if y > x:
                    for z in adj[y]:
                        if z > y and z in adj[x]:
                            for w in adj[z]:
                                if w > z and w in adj[x] and w in adj[y]:
                                    k4s.add(tuple(sorted((x, y, z, w))))
        
        for k in k4s:
            w_new = self.next_node
            self.next_node += 1
            self.nodes.add(w_new)
            new_edges.update([(min(k[0], w_new), max(k[0], w_new)),
                              (min(k[1], w_new), max(k[1], w_new)),
                              (min(k[2], w_new), max(k[2], w_new))])
                              
        for e in edges_to_remove:
            new_edges.discard(e)
            
        self.edges = new_edges

print("K3")
sim = PurePythonHypergraphEngine([(1,2), (2,3), (1,3)])
for _ in range(5):
    sim.step()
    print(len(sim.edges))

print("K4")
sim = PurePythonHypergraphEngine([(1,2), (2,3), (3,1), (1,4), (2,4), (3,4)])
for _ in range(5):
    sim.step()
    print(len(sim.edges))

print("K5")
sim = PurePythonHypergraphEngine([(1,2), (1,3), (1,4), (1,5), (2,3), (2,4), (2,5), (3,4), (3,5), (4,5)])
for _ in range(5):
    sim.step()
    print(len(sim.edges))

