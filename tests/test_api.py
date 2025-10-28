from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_endpoint():
    r = client.get("/api/add", params={"a": 2, "b": 3})
    assert r.status_code == 200
    assert r.json()["result"] == 5.0

def test_subtract_endpoint():
    r = client.get("/api/subtract", params={"a": 5, "b": 10})
    assert r.status_code == 200
    assert r.json()["result"] == -5.0

def test_multiply_endpoint():
    r = client.get("/api/multiply", params={"a": 3, "b": 2.5})
    assert r.status_code == 200
    assert r.json()["result"] == 7.5

def test_divide_endpoint_ok():
    r = client.get("/api/divide", params={"a": 9, "b": 2})
    assert r.status_code == 200
    assert r.json()["result"] == 4.5

def test_divide_endpoint_by_zero():
    r = client.get("/api/divide", params={"a": 9, "b": 0})
    assert r.status_code == 400
    assert "Division by zero" in r.json()["detail"]
