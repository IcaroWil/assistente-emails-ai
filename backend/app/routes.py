from fastapi import APIRouter, UploadFile, File, HTTPException
from .schemas import EmailInput, ProcessedResult, HealthResponse, ClassifyTopK
from .classifier import classify_email
from .responder import generate_response, get_labels
from .utils import text_from_upload
from .config import settings

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok", "model": settings.HF_MODEL_NAME}

@router.get("/labels")
def labels():
    return {"labels": get_labels()}

@router.post("/process", response_model=ProcessedResult)
def process_body(email: EmailInput):
    result = classify_email(email.text)
    resposta = generate_response(result["categoria"])
    return {**result, "resposta": resposta}

@router.post("/upload", response_model=ProcessedResult)
async def process_upload(file: UploadFile = File(...)):
    text = await text_from_upload(file)
    if not text.strip():
        raise HTTPException(status_code=400, detail="Arquivo sem texto extraível.")
    result = classify_email(text)
    resposta = generate_response(result["categoria"])
    return {**result, "resposta": resposta}
