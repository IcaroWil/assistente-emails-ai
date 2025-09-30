from fastapi.testclient import TestClient
from backend.uvicorn_app import app

client = TestClient(app)

def test_process_produtivo():
    r = client.post("/process", json={"texto":"Estou com erro 500 no checkout"})
    assert r.status_code == 200
    assert r.json()["categoria"] == "Produtivo"

def test_process_improdutivo():
    r = client.post("/process", json={"texto":"Bom dia! Ótima semana!"})
    assert r.status_code == 200
    assert r.json()["categoria"] == "Improdutivo"
