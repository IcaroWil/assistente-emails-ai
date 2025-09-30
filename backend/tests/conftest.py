# backend/tests/conftest.py
import re
import pytest
from unittest.mock import Mock
import backend.app.classifier as clf

@pytest.fixture(autouse=True)
def mock_hf(monkeypatch):
    """Mocka a chamada à Hugging Face só durante os testes."""
    prod_patterns = [re.compile(p) for p in clf.PRODUCTIVE_HINTS]
    imp_patterns  = [re.compile(p) for p in clf.IMPRODUCTIVE_HINTS]

    def fake_post(url, headers=None, json=None, timeout=30):
        txt = (json or {}).get("inputs", "") or ""
        norm = txt.lower()

        is_prod = any(p.search(norm) for p in prod_patterns)
        is_imp  = any(p.search(norm) for p in imp_patterns)

        if is_prod and not is_imp:
            label = clf.CANDIDATE_EN[0]
            score = 0.92
        elif is_imp and not is_prod:
            label = clf.NON_ACTION_EN
            score = 0.94
        else:
            label = clf.NON_ACTION_EN
            score = 0.60

        m = Mock()
        m.raise_for_status = lambda: None
        m.json = lambda: {"labels": [label], "scores": [score]}
        return m

    monkeypatch.setattr(clf._session, "post", fake_post)
