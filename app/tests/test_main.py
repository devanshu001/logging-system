from datetime import datetime
import json

def test_health_check(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_ingest_log(client):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "level": "ERROR",
        "message": "Test log message",
        "service": "test-service"
    }
    response = client.post("/logs", json=log_data)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["status"] == "Log queued successfully"

def test_query_logs(client):
    response = client.get("/logs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_aggregation(client):
    response = client.get("/logs/aggregations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
