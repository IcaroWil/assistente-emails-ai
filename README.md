# Assistente Email AI

Classifica emails entre **Produtivo** e **Improdutivo** e sugere uma **resposta automática**.  
Stack: **FastAPI**, **Hugging Face Inference API** (zero-shot), **HTML/CSS/JS**.

## Demo
- **Frontend:** https://assistente-emails-ai.vercel.app/
- **Backend (API):** https://assistente-emails-ai.onrender.com/docs

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
- `GET /health` – `{ "status": "ok", "model": "..." }`
- `POST /process` – body: `{ "texto": "..." }`  
  resposta: `{ "categoria": "Produtivo|Improdutivo", "score": 0.93, "resposta": "..." }`
- `POST /upload` – `multipart/form-data` com `file` (`.txt` ou `.pdf`)

---

## Como funciona (resumo técnico)
1. **Classificação**: chama a **Hugging Face Inference API** com um conjunto de rótulos descritivos em inglês
   (ex.: “actionable bug report…”, “non-actionable…”) e mapeia para **Produtivo/Improdutivo**.
2. **Pós-filtro leve**: regex em PT corrige casos clássicos (ex.: “erro 500”, “fatura”, “acesso bloqueado”, “#12345”).
3. **Resposta automática**: `responder.py` monta a resposta de acordo com a categoria.
4. **Uploads**: `pypdf` extrai texto de PDFs.

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