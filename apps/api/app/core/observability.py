import json
import logging
import re
import threading
from collections import defaultdict
from time import time
from uuid import uuid4

REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9._-]{1,100}$")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": time(),
            "level": record.levelname.lower(),
            "logger": record.name,
            "message": record.getMessage(),
        }
        for field in ("request_id", "method", "route", "status_code", "duration_ms", "user_id"):
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def configure_json_logging() -> None:
    root = logging.getLogger()
    if not root.handlers:
        root.addHandler(logging.StreamHandler())
    formatter = JsonFormatter()
    for handler in root.handlers:
        handler.setFormatter(formatter)
    root.setLevel(logging.INFO)


class Metrics:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._requests: dict[tuple[str, str, int], int] = defaultdict(int)
        self._duration_sum: dict[tuple[str, str], float] = defaultdict(float)
        self._duration_count: dict[tuple[str, str], int] = defaultdict(int)
        self._business: dict[tuple[str, tuple[tuple[str, str], ...]], int] = defaultdict(int)
        self._gauges: dict[tuple[str, tuple[tuple[str, str], ...]], float] = {}

    def observe_request(self, method: str, route: str, status_code: int, duration: float) -> None:
        with self._lock:
            self._requests[(method, route, status_code)] += 1
            self._duration_sum[(method, route)] += duration
            self._duration_count[(method, route)] += 1

    def increment(self, metric: str, **labels: str) -> None:
        with self._lock:
            self._business[(metric, tuple(sorted(labels.items())))] += 1

    def set_gauge(self, metric: str, value: float, **labels: str) -> None:
        with self._lock:
            self._gauges[(metric, tuple(sorted(labels.items())))] = value

    def render(self) -> str:
        lines = [
            "# HELP ilex_http_requests_total HTTP requests processed.",
            "# TYPE ilex_http_requests_total counter",
        ]
        with self._lock:
            for (method, route, status_code), value in sorted(self._requests.items()):
                lines.append(
                    f'ilex_http_requests_total{{method="{method}",route="{route}",status="{status_code}"}} {value}'
                )
            lines.extend(
                [
                    "# HELP ilex_http_request_duration_seconds HTTP request latency.",
                    "# TYPE ilex_http_request_duration_seconds summary",
                ]
            )
            for (method, route), value in sorted(self._duration_sum.items()):
                labels = f'method="{method}",route="{route}"'
                lines.append(f"ilex_http_request_duration_seconds_sum{{{labels}}} {value:.6f}")
                lines.append(f"ilex_http_request_duration_seconds_count{{{labels}}} {self._duration_count[(method, route)]}")
            for (metric, labels), value in sorted(self._business.items()):
                rendered_labels = ",".join(f'{key}="{item}"' for key, item in labels)
                suffix = f"{{{rendered_labels}}}" if rendered_labels else ""
                lines.append(f"ilex_{metric}_total{suffix} {value}")
            for (metric, labels), value in sorted(self._gauges.items()):
                rendered_labels = ",".join(f'{key}="{item}"' for key, item in labels)
                suffix = f"{{{rendered_labels}}}" if rendered_labels else ""
                lines.append(f"ilex_{metric}{suffix} {value}")
        return "\n".join(lines) + "\n"


metrics = Metrics()


def request_id_from_header(value: str | None) -> str:
    return value if value and REQUEST_ID_PATTERN.fullmatch(value) else str(uuid4())
