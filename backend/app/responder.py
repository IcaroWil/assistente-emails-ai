from .config import settings

def generate_response(category: str) -> str:
    if category == "Produtivo":
        return (
            "Obrigado pelo contato. Registramos sua solicitação e retornaremos com uma "
            "atualização até o fim do dia útil. Caso tenha anexos ou número do chamado, "
            "por favor responda a este e-mail com essas informações."
        )

    return (
        "Agradecemos a mensagem! Não é necessária nenhuma ação neste momento. "
        "Estamos à disposição."
    )

def get_labels():
    return settings.CANDIDATE_LABELS
