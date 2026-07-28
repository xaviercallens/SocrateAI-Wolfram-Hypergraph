"""
Cloud Run HTTP MCP Entrypoint for Wolfram CAG Engine
Exposes HTTP REST endpoints for Model Context Protocol execution.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import sys
from pathlib import Path

# Add project root to sys.path
root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from agents.cosmology_agent.cosmology_agent import CosmologyAgent

class MCPHTTPRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, data: dict):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path == "/health" or self.path == "/":
            self._send_json(200, {"status": "HEALTHY", "mcp_service": "wolfram-engine-cag"})
        else:
            self._send_json(404, {"error": "Not Found"})

    def do_POST(self):
        if self.path == "/mcp/execute":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode("utf-8")
            try:
                req = json.loads(body)
                prompt = req.get("prompt", "Calculate vacuum energy")
                agent = CosmologyAgent()
                result = agent.route_query(prompt)
                self._send_json(200, result)
            except Exception as e:
                self._send_json(500, {"error": str(e)})
        else:
            self._send_json(404, {"error": "Endpoint not found"})

def run_server(port: int = 8080):
    server = HTTPServer(("0.0.0.0", port), MCPHTTPRequestHandler)
    print(f"Wolfram CAG MCP Microservice listening on port {port}...")
    server.serve_forever()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    run_server(port)
