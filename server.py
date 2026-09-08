"""Minimal stats HTTP server for the tests repo.

Exposes a single health/ping route used by the E2E pipeline:
    GET /ping -> 200 {"pong": true}

Run (default port 8080):
    python3 server.py
Override the port with the PORT environment variable.
"""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8080"))

STATUS_OK = 200
STATUS_NOT_FOUND = 404


class Handler(BaseHTTPRequestHandler):
    """Request handler for the ping route."""

    def do_GET(self):
        """Dispatch GET requests to the ping route."""
        if self.path.rstrip("/") == "/ping":
            self._respond(STATUS_OK, {"pong": True})
        else:
            self._respond(STATUS_NOT_FOUND, {"error": "not found"})

    def _respond(self, status, payload):
        """Send a JSON response with the given status code and body."""
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        """Quiet request logging (keeps test output clean)."""
        print(f"[ping-server] {self.address_string()} - {format % args}")


def run():
    """Start the server and serve until interrupted."""
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"[ping-server] listening on http://{HOST}:{PORT}/ping")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run()