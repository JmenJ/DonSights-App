import json
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler

class JSONHandler(BaseHTTPRequestHandler):
    """
    A very simple HTTP(S) request handler that serves JSON responses.
    It implements a GET endpoint at /ping and echoes JSON bodies on POST.

    This handler avoids external frameworks like Flask or Django and instead
    uses Python's built‑in http.server module to handle incoming requests.
    """

    def _send_json(self, obj: dict, status: int = 200) -> None:
        """Utility to send a JSON response with a given status code."""
        payload = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:
        """Handle GET requests."""
        if self.path == "/ping":
            # Respond with a simple JSON object.
            self._send_json({"message": "pong", "status": "ok"})
        else:
            # Unknown path: return 404.
            self._send_json({"error": "Not found"}, status=404)

    def do_POST(self) -> None:
        """Handle POST requests by echoing back the JSON payload."""
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body.decode("utf-8")) if body else {}
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON"}, status=400)
            return
        # Augment the payload to show it was processed.
        data["received"] = True
        self._send_json(data, status=200)


def run_server() -> None:
    """
    Configure and run an HTTPS server on port 4443.  A self‑signed certificate
    (`cert.pem`) and private key (`key.pem`) must exist in the working directory.

    The server binds to all interfaces (0.0.0.0) so it is reachable both from
    your host machine and other containers on the same network.
    """
    host = ""
    port = 4443
    httpd = HTTPServer((host, port), JSONHandler)

    # Wrap the underlying socket in SSL/TLS.  The AnvilEight blog shows how
    # to use ssl.wrap_socket to add HTTPS support to HTTPServer【789800368038483†L62-L76】.
    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        keyfile="key.pem",
        certfile="cert.pem",
        server_side=True,
    )

    print(f"Serving HTTPS on 0.0.0.0:{port} …")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
