import sys

with open("agents/topology_agent/topology_agent.py", "r") as f:
    code = f.read()

old = """        results = {}
        for seed_name, seed_data in seeds.items():
            engine = PurePythonHypergraphEngine(seeds_edges[seed_name])"""
new = """        results = {}
        for seed_name, seed_data in seeds.items():
            density_rate = seed_data["density_rate"]
            engine = PurePythonHypergraphEngine(seeds_edges[seed_name])"""
            
code = code.replace(old, new)

with open("agents/topology_agent/topology_agent.py", "w") as f:
    f.write(code)

with open("tests/test_twobody_attraction.py", "r") as f:
    test_code = f.read()
    
test_code = test_code.replace("== 10.0", "== 3.0")

with open("tests/test_twobody_attraction.py", "w") as f:
    f.write(test_code)

