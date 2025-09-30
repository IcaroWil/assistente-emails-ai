# Assistente Email AI

Classifica emails entre **Produtivo** e **Improdutivo** e sugere uma **resposta automática**.  
Stack: **FastAPI**, **Transformers (zero-shot)**, **HTML/CSS/JS**.

## Demo
- **Frontend:** _coloque aqui o link (Vercel/Netlify)_
- **Backend (API):** _coloque aqui o link (Render)_

> No frontend, você pode passar a URL da API por query string:
> `https://seu-front.vercel.app/?api=https://SEU-BACKEND.onrender.com`

---

## Rodando local

### 1. Depêndencias
```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. API (FastAPI)
```bash
uvicorn backend.uvicorn_app:app --reload
# http://127.0.0.1:8000/docs
```

### 3. Frontend estático
```bash
cd frontend
python -m http.server 5173
# http://localhost:5173
```

---

## Testes
Rápido (sem baixar modelo):
```bash
# Windows PowerShell
$env:MOCK_HF="1"
pytest -q

# Linux/macOS
MOCK_HF=1 pytest -q
```

Reais (com modelo):
```bash
pytest -q
```

---

## Endpoints
- `GET /` – ping
- `GET /health` - `{ status, model }`
- `POST /process` - body: `{ "text": "..." }`
resposta: `{ "categoria": "Produtivo|Improdutivo", "score": 0.93, "resposta": "..." }`
- `POST /upload` - `multipart/form-data` com `file` (`.txt` ou `.pdf`)

---

## Como funciona (resumo técnico)
1. Pré-processamento (`app/preprocess.py`): normaliza texto, remove URLs/emails, quoted lines, pontuação.
2. Classificação (`app/classifier.py`): `zero-shot-classification` com `HF_HYPOTHESIS_PT="Este texto é {}."` e labels `["Produtivo","Improdutivo"]`
3. Resposta automática (`app/responder.py`): template simples por categoria.
4. Uploads (`app/utils.py`): extrai texto de `.txt` e `.pdf` via `pypdf`.
5. API (`uvicorn_app.py` + `app/routes.py`): FastAPI com CORS aberto para o front.

---

## Deploy (Render)
- Build: `pip install -r backend/requirements.txt`
- Start: `uvicorn backend.uvicorn_app:app --host 0.0.0.0 --port $PORT`
- ENVs sugeridas:
    - `CORS_ORIGINS=*`
    - `HF_HYPOTHESIS_PT=Este texto é {}`
    - `HF_MODEL_NAME=valhalla/distilbart-mnli-12-1`

---

## Dev
- CI: GitHub Actions rodando testes com `MOCK_HF=1`
- Docker:
```bash
docker build -t email-ai-classifier .
docker run -p 8000:8000 email-ai-classifier
```
- Makefile:
    - `make install`, `make run`, `make test`, `make docker-build`, `make docker-run`