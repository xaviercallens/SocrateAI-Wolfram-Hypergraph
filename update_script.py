import sys
content = open("agents/topology_agent/topology_agent.py").read()

new_classes = """import json
import torch
import math
from typing import Dict, Any

class PurePythonHypergraphEngine:
    def __init__(self, edges):
        self.edges = set(tuple(sorted(e)) for e in edges)
        self.nodes = set(n for e in edges for n in e)
        self.next_node = max(self.nodes) + 1 if self.nodes else 1

    def step_mass_spectrum(self):
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

    def step_attraction(self, t1_nodes, t2_nodes):
        # Simulates geodesic contraction by finding the shortest path and shortcutting it
        adj = {n: set() for n in self.nodes}
        for u, v in self.edges:
            adj[u].add(v)
            adj[v].add(u)
        
        # simple BFS to find distance
        visited = {n: -1 for n in self.nodes}
        queue = []
        for n in t1_nodes:
            visited[n] = 0
            queue.append(n)
        
        while queue:
            curr = queue.pop(0)
            if curr in t2_nodes:
                break
            for nxt in adj[curr]:
                if visited[nxt] == -1:
                    visited[nxt] = visited[curr] + 1
                    queue.append(nxt)
        
        # Shortcut: add an edge between random t1 and a closer node
        for n in t2_nodes:
            if visited[n] != -1 and visited[n] > 1:
                # Add edge to shorten
                w = self.next_node
                self.next_node += 1
                self.nodes.add(w)
                self.edges.add((list(t1_nodes)[0], w))
                self.edges.add((w, n))
                break

    def get_distance(self, t1_nodes, t2_nodes):
        adj = {n: set() for n in self.nodes}
        for u, v in self.edges:
            adj[u].add(v)
            adj[v].add(u)
        visited = {n: -1 for n in self.nodes}
        queue = []
        for n in t1_nodes:
            visited[n] = 0
            queue.append(n)
        min_dist = float('inf')
        while queue:
            curr = queue.pop(0)
            if curr in t2_nodes:
                min_dist = min(min_dist, visited[curr])
            for nxt in adj[curr]:
                if visited[nxt] == -1:
                    visited[nxt] = visited[curr] + 1
                    queue.append(nxt)
        return min_dist if min_dist != float('inf') else 10.0
"""

content = content.replace("import json\nimport torch\nfrom typing import Dict, Any", new_classes)

with open("agents/topology_agent/topology_agent.py", "w") as f:
    f.write(content)
