import os
import random
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.error import URLError

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("proxy")

MONOLITH_URL = os.getenv("MONOLITH_URL", "http://monolith:8080")
MOVIES_SERVICE_URL = os.getenv("MOVIES_SERVICE_URL", "http://movies-service:8081")
EVENTS_SERVICE_URL = os.getenv("EVENTS_SERVICE_URL", "http://events-service:8082")
GRADUAL_MIGRATION = os.getenv("GRADUAL_MIGRATION", "true").lower() == "true"
MOVIES_MIGRATION_PERCENT = int(os.getenv("MOVIES_MIGRATION_PERCENT", "50"))
PORT = int(os.getenv("PORT", "8000"))


class ProxyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self._proxy()

    def do_POST(self):
        self._proxy()

    def do_PUT(self):
        self._proxy()

    def do_DELETE(self):
        self._proxy()

    def _proxy(self):
        path = self.path

        # Health check
        if path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Strangler Fig Proxy is healthy")
            return

        # Route /api/events/* -> events service
        if path.startswith("/api/events"):
            self._forward(EVENTS_SERVICE_URL)
            return

        # Route /api/movies* -> movies service or monolith
        if path.startswith("/api/movies"):
            if self._should_route_to_microservice():
                logger.info("Routing %s %s -> Movies Service", self.command, path)
                self._forward(MOVIES_SERVICE_URL)
            else:
                logger.info("Routing %s %s -> Monolith", self.command, path)
                self._forward(MONOLITH_URL)
            return

        # Everything else -> monolith
        self._forward(MONOLITH_URL)

    def _should_route_to_microservice(self):
        if not GRADUAL_MIGRATION:
            return True
        return random.randint(0, 99) < MOVIES_MIGRATION_PERCENT

    def _forward(self, target_base_url):
        target_url = target_base_url + self.path

        # Read request body
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        req = Request(target_url, data=body, method=self.command)

        # Copy headers (skip hop-by-hop)
        skip_headers = {"host", "connection", "transfer-encoding", "content-length"}
        for key, value in self.headers.items():
            if key.lower() not in skip_headers:
                req.add_header(key, value)
        if body is not None:
            req.add_header("Content-Length", str(len(body)))

        try:
            with urlopen(req, timeout=30) as resp:
                resp_body = resp.read()
                self.send_response(resp.status)
                for key, value in resp.getheaders():
                    if key.lower() not in ("transfer-encoding", "connection"):
                        self.send_header(key, value)
                self.end_headers()
                self.wfile.write(resp_body)
        except URLError as e:
            logger.error("Upstream error for %s: %s", target_url, e)
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error":"Upstream service unavailable"}')

    def log_message(self, format, *args):
        logger.info(format, *args)


if __name__ == "__main__":
    logger.info(
        "Proxy started: GRADUAL_MIGRATION=%s, MOVIES_MIGRATION_PERCENT=%d",
        GRADUAL_MIGRATION, MOVIES_MIGRATION_PERCENT,
    )
    logger.info(
        "MONOLITH_URL=%s, MOVIES_SERVICE_URL=%s, EVENTS_SERVICE_URL=%s",
        MONOLITH_URL, MOVIES_SERVICE_URL, EVENTS_SERVICE_URL,
    )
    server = HTTPServer(("0.0.0.0", PORT), ProxyHandler)
    logger.info("Proxy listening on port %d", PORT)
    server.serve_forever()
