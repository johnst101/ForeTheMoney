#!/usr/bin/env python3
"""Smoke test for a deployed backend: exits 0 only if GET <base_url>/health returns 200 {"status": "ok"}."""

import json
import sys
import urllib.error
import urllib.request

REQUEST_TIMEOUT_SECONDS = 10


def check_health(base_url: str) -> str | None:
    """Return None if the service is healthy, otherwise a short reason for the failure."""
    url = f"{base_url.rstrip('/')}/health"
    try:
        with urllib.request.urlopen(url, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            status = response.status
            body = response.read()
    except urllib.error.HTTPError as exc:
        return f"{url} returned HTTP {exc.code}"
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return f"{url} is unreachable: {exc}"

    if status != 200:
        return f"{url} returned HTTP {status}"

    try:
        payload = json.loads(body)
    except ValueError:
        return f"{url} returned a non-JSON body"

    if payload != {"status": "ok"}:
        return f'{url} returned unexpected body, expected {{"status": "ok"}}'

    return None


def main(argv: list[str]) -> int:
    """CLI entry point; returns 0 if healthy, 1 if unhealthy, 2 on bad usage."""
    if len(argv) != 2:
        print(f"usage: {argv[0]} <base_url>", file=sys.stderr)
        return 2

    failure = check_health(argv[1])
    if failure is not None:
        print(f"SMOKE TEST FAILED: {failure}", file=sys.stderr)
        return 1

    print("SMOKE TEST PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
