from backend.app.responder import generate_response

def test_respostas_basicas():
    assert "Obrigado" in generate_response("Produtivo")
    assert "Agradecemos" in generate_response("Improdutivo")
