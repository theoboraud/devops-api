from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_readyz():
    r = client.get("/readyz")
    assert r.status_code == 200
    assert r.json()["status"] == "ready"

def test_metrics():
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "http_requests_total" in r.text
