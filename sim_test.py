import random

class MultiwaySim:
    def __init__(self, edges):
        self.edges = set(tuple(sorted(e)) for e in edges)
        self.nodes = set(n for e in edges for n in e)
        self.next_node = max(self.nodes) + 1 if self.nodes else 1

    def step(self):
        # deterministic or randomized? Let's do random.
        adj = {n: set() for n in self.nodes}
        for u, v in self.edges:
            adj[u].add(v)
            adj[v].add(u)

        # Find triangles
        triangles = set()
        for x in self.nodes:
            for y in adj[x]:
                if y > x:
                    for z in adj[y]:
                        if z > y and z in adj[x]:
                            triangles.add((x, y, z))
        
        # Find V-shapes
        v_shapes = set()
        for x in self.nodes:
            neighbors = list(adj[x])
            for i in range(len(neighbors)):
                for j in range(i+1, len(neighbors)):
                    y, z = sorted([neighbors[i], neighbors[j]])
                    v_shapes.add((x, y, z))

        # Apply Rule A (Vacuum expansion): picks a random V-shape, destroys 2 edges, adds 3.
        # Apply Rule B (Gravity): picks a random triangle, adds 3 edges.
        
        if triangles and random.random() < 0.8: # Rule B has 80% chance if triangles exist
            t = random.choice(list(triangles))
            w = self.next_node
            self.next_node += 1
            self.nodes.add(w)
            self.edges.update([(min(t[0], w), max(t[0], w)), 
                               (min(t[1], w), max(t[1], w)), 
                               (min(t[2], w), max(t[2], w))])
        
        if v_shapes and random.random() < 0.5: # Rule A
            v = random.choice(list(v_shapes))
            x, y, z = v # x is center
            e1 = tuple(sorted([x, y]))
            e2 = tuple(sorted([x, z]))
            if e1 in self.edges and e2 in self.edges:
                self.edges.remove(e1)
                self.edges.remove(e2)
                w = self.next_node
                self.next_node += 1
                self.nodes.add(w)
                self.edges.update([(min(x, w), max(x, w)), 
                                   (min(y, w), max(y, w)), 
                                   (min(z, w), max(z, w))])

k3 = [(1,2), (2,3), (1,3)]
sim = MultiwaySim(k3)
for _ in range(10):
    sim.step()
    print("K3 edges:", len(sim.edges))
