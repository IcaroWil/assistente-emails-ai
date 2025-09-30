from backend.app.classifier import classify_email

def test_returns_known_labels():
    txt = "Preciso de ajuda com o sistema, não consigo acessar minha conta"
    res = classify_email(txt)
    assert res["categoria"] in {"Produtivo", "Improdutivo"}
    assert 0.0 <= res["score"] <= 1.0