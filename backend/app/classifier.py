import re
import unicodedata
import requests
from typing import Dict
from .config import settings

_session = requests.Session()

INTERNAL_LABELS = {
    "prod_access": "actionable support request: account access blocked or login/permission issue",
    "prod_billing": "actionable billing request: invoice reissue, payment or charge question",
    "prod_bug": "actionable bug report or system error (error code, cannot complete task)",
    "prod_status": "actionable request: status update for an existing ticket or order",
    "non_action": "non-actionable message: greeting, thanks, promotion, newsletter, meme"
}
CANDIDATE_EN = list(INTERNAL_LABELS.values())
NON_ACTION_EN = INTERNAL_LABELS["non_action"]

PRODUCTIVE_HINTS = [
    r"\berro\b", r"\berror\b", r"\b\d{3}\b",
    r"\bfalhou?\b", r"\bnao consigo\b", r"\bn[aã]o consigo\b",
    r"\bacesso\b", r"\bbloquead", r"\blogin\b", r"\bpermiss[aã]o\b", r"\bliberar\b",
    r"\breset(ar)? senha\b",
    r"\bfatura\b", r"\bnota fiscal\b", r"\bcobran[çc]a\b", r"\breemit",
    r"\banexo\b", r"\banex[ao]s\b",
    r"\bstatus\b", r"\bchamado\b", r"#\d+",
    r"\bpedido\b", r"\bcheckout\b", r"\bvalidar\b",
]
IMPRODUCTIVE_HINTS = [
    r"\bbom dia\b", r"\bboa tarde\b", r"\bboa noite\b",
    r"\bobrigad[oa]\b", r"\bagradec",
    r"\bpromo[cç][aã]o\b", r"%", r"\bdesconto\b", r"\bnewsletter\b",
    r"\bmeme\b", r"\bhappy hour\b", r"\bignore\b", r"\bf[ée]rias\b"
]

def _normalize(s: str) -> str:
    s = s.lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s

def _hf_headers():
    h = {"Content-Type": "application/json"}
    if settings.HF_API_TOKEN:
        h["Authorization"] = f"Bearer {settings.HF_API_TOKEN}"
    return h

def classify_email(text: str) -> Dict[str, float | str]:
    raw = (text or "").strip()
    norm = _normalize(raw)

    payload = {
        "inputs": raw,
        "parameters": {
            "candidate_labels": CANDIDATE_EN,
            "hypothesis_template": "This email is {}.",
            "multi_label": False
        },
        "options": {"wait_for_model": True, "use_cache": True}
    }
    url = f"{settings.HF_API_BASE.rstrip('/')}/{settings.HF_MODEL_NAME}"
    resp = _session.post(url, headers=_hf_headers(), json=payload, timeout=30)
    resp.raise_for_status()
    out = resp.json()

    labels = out.get("labels") or []
    scores = out.get("scores") or []
    if not labels or not scores:
        raise RuntimeError(f"Unexpected HF response: {out}")

    label_en = labels[0]
    score = float(scores[0])
    categoria = "Improdutivo" if label_en == NON_ACTION_EN else "Produtivo"

    low = score < 0.70

    if any(re.search(p, norm) for p in PRODUCTIVE_HINTS):
        if categoria == "Improdutivo" or low:
            categoria = "Produtivo"

    if any(re.search(p, norm) for p in IMPRODUCTIVE_HINTS):
        if categoria == "Produtivo" and low:
            categoria = "Improdutivo"

    return {"categoria": categoria, "score": score}
