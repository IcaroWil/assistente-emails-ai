import os
from transformers import pipeline, Pipeline
from .preprocess import clean_text
from .config import settings
from typing import Dict

_classifier: Pipeline | None = None

def get_classifier() -> Pipeline:
    global _classifier
    if _classifier is None:
        if os.getenv("MOCK_HF", "0") == "1":
            class Fake:
                def __call__(self, text, candidate_labels, **kw):
                    text = (text or "").lower()
                    produtivo_kw = ["suporte","erro","acesso","chamado","fatura","cobrança","status"]
                    label = "Produtivo" if any(k in text for k in produtivo_kw) else "Improdutivo"
                    return {"labels": [label], "scores": [0.9]}
            _classifier = Fake()
        else:
            _classifier = pipeline(task=settings.HF_TASK, model=settings.HF_MODEL_NAME)
    return _classifier

def classify_email(text: str) -> Dict[str, float | str]:
    text_clean = clean_text(text)
    clf = get_classifier()
    template = settings.HF_HYPOTHESIS_PT
    if "{label}" in template:
        template = template.replace("{label}", "{}")

    result = clf(
        text_clean,
        candidate_labels=settings.CANDIDATE_LABELS,
        hypothesis_template=template,
        multi_label=False,
    )
    label = result["labels"][0]
    score = float(result["scores"][0])
    return {"categoria": label, "score": score}
