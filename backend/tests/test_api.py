from fastapi.testclient import TestClient
from backend.uvicorn_app import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_process():
    r = client.post("/process", json={"text": "Status do meu chamado 123"})
    assert r.status_code == 200
    payload = r.json()
    assert "categoria" in payload and "resposta" in payload