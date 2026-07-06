#!/usr/bin/env python3
"""Read-only smoke checks for an Ilex staging/production deployment."""

import json
import os
import sys
import urllib.error
import urllib.request


def check(url: str, token: str | None = None) -> tuple[int, str]:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.status, response.read(500).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(500).decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        return 0, str(exc.reason)


def main() -> int:
    base = os.environ.get("ILEX_SMOKE_BASE_URL", "").rstrip("/")
    token = os.environ.get("ILEX_SMOKE_TOKEN")
    if not base or not token:
        print("ILEX_SMOKE_BASE_URL e ILEX_SMOKE_TOKEN sao obrigatorios", file=sys.stderr)
        return 2
    checks = {
        "web": (base, None),
        "liveness": (f"{base}/api/v1/health/live", None),
        "readiness": (f"{base}/api/v1/health/ready", None),
        "orders": (f"{base}/api/v1/orders?page=1&page_size=1", token),
        "carriers": (f"{base}/api/v1/carriers", token),
        "dashboard": (f"{base}/api/v1/dashboard/summary", token),
        "audit": (f"{base}/api/v1/audit?page=1&page_size=1", token),
    }
    results = {name: {"status": status, "body": body} for name, (url, auth) in checks.items() for status, body in [check(url, auth)]}
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return int(any(item["status"] < 200 or item["status"] >= 400 for item in results.values()))


if __name__ == "__main__":
    raise SystemExit(main())
