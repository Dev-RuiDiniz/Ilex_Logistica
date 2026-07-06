#!/usr/bin/env python3
"""Reproducible HTTP performance gate for a production-like Ilex environment."""

import argparse
import concurrent.futures
import json
import statistics
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass


@dataclass
class Result:
    scenario: str
    requests: int
    errors: int
    p50_ms: float
    p95_ms: float
    p99_ms: float
    throughput_rps: float


def percentile(values: list[float], percentile_value: int) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((percentile_value / 100) * (len(ordered) - 1))))
    return ordered[index]


def request_once(url: str, token: str) -> tuple[float, bool]:
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            response.read()
            success = response.status < 500
    except (urllib.error.URLError, TimeoutError):
        success = False
    return (time.perf_counter() - started) * 1000, success


def run_scenario(name: str, url: str, token: str, requests: int, concurrency: int) -> Result:
    started = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as pool:
        samples = list(pool.map(lambda _: request_once(url, token), range(requests)))
    elapsed = time.perf_counter() - started
    timings = [timing for timing, _ in samples]
    return Result(
        scenario=name,
        requests=requests,
        errors=sum(not success for _, success in samples),
        p50_ms=round(statistics.median(timings), 2),
        p95_ms=round(percentile(timings, 95), 2),
        p99_ms=round(percentile(timings, 99), 2),
        throughput_rps=round(requests / elapsed, 2),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--token", required=True)
    parser.add_argument("--requests", type=int, default=500)
    parser.add_argument("--concurrency", type=int, default=50)
    parser.add_argument("--output")
    args = parser.parse_args()
    base = args.base_url.rstrip("/")
    scenarios = {
        "orders_filtered": f"{base}/orders?page=1&page_size=20&status=active",
        "dashboard": f"{base}/dashboard/summary",
        "shipments_filtered": f"{base}/shipments?page=1&page_size=20",
    }
    results = [
        run_scenario(name, url, args.token, args.requests, args.concurrency)
        for name, url in scenarios.items()
    ]
    payload = {"concurrency": args.concurrency, "results": [asdict(result) for result in results]}
    rendered = json.dumps(payload, indent=2)
    print(rendered)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as stream:
            stream.write(rendered + "\n")
    return int(any(result.errors or result.p95_ms > 1000 for result in results))


if __name__ == "__main__":
    raise SystemExit(main())
