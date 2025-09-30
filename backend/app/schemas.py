from pydantic import BaseModel, Field
from typing import List, Optional

class EmailInput(BaseModel):
    text: str = Field(..., min_length=1)

class ProcessedResult(BaseModel):
    categoria: str
    score: float
    resposta: str

class HealthResponse(BaseModel):
    status: str
    model: str

class ClassifyTopK(BaseModel):
    labels: List[str]
    scores: List[float]

class ErrorResponse(BaseModel):
    detail: str
