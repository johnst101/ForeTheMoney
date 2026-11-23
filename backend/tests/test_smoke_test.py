"""Tests scripts/smoke_test.py through its CLI against a local stub server."""

import json
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

SMOKE_TEST = Path(__file__).resolve().parents[2] / "scripts" / "smoke_test.py"


@pytest.fixture
def stub_server():
    """Start a local server whose /health reply is set by the test; yields (base_url, set_reply)."""
    reply = {"status": 200, "body": b'{"status": "ok"}'}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(reply["status"])
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(reply["body"])

        def log_message(self, *args):
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    def set_reply(status: int, body: dict | bytes):
        reply["status"] = status
        reply["body"] = body if isinstance(body, bytes) else json.dumps(body).encode()

    yield f"http://127.0.0.1:{server.server_port}", set_reply

    server.shutdown()
    server.server_close()


def run_smoke_test(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SMOKE_TEST), *args],
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_smoke_test_passes_against_healthy_service(stub_server):
    base_url, _ = stub_server

    result = run_smoke_test(base_url)

    assert result.returncode == 0


def test_smoke_test_fails_on_non_200_status(stub_server):
    base_url, set_reply = stub_server
    set_reply(503, {"status": "ok"})

    result = run_smoke_test(base_url)

    assert result.returncode != 0
    assert "503" in result.stderr


def test_smoke_test_fails_on_unexpected_body(stub_server):
    base_url, set_reply = stub_server
    set_reply(200, {"status": "degraded"})

    result = run_smoke_test(base_url)

    assert result.returncode != 0
    assert result.stderr.strip()


def test_smoke_test_fails_when_target_unreachable():
    result = run_smoke_test("http://127.0.0.1:1")

    assert result.returncode != 0
    assert result.stderr.strip()
