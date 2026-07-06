def test_request_id_and_metrics_are_exposed(client) -> None:
    response = client.get("/health", headers={"X-Request-ID": "test-request-123"})
    assert response.headers["x-request-id"] == "test-request-123"

    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    assert "ilex_http_requests_total" in metrics.text
    assert "ilex_http_request_duration_seconds" in metrics.text


def test_liveness_and_readiness_are_distinct(client) -> None:
    live = client.get("/api/v1/health/live")
    ready = client.get("/api/v1/health/ready")
    assert live.status_code == 200
    assert live.json() == {"status": "alive"}
    assert ready.status_code == 200
    assert ready.json()["status"] == "ready"
    assert ready.json()["postgresql"] is True
