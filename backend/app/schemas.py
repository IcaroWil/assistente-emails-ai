from pydantic import BaseModel, Field, ConfigDict, AliasChoices
from typing import List, Optional

class EmailInput(BaseModel):
    model_config = ConfigDict(extra="ignore")
    text: str = Field(..., min_length=1,
                validation_alias=AliasChoices("texto", "text"))

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
