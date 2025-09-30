import json
from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "Email Classifier API"
    DEBUG: bool = False

    HF_MODEL_NAME: str = "facebook/bart-large-mnli"
    HF_TASK: str = "zero-shot-classification"
    HF_HYPOTHESIS_PT: str = "Este texto é {}."

    CANDIDATE_LABELS: List[str] = Field(default_factory=lambda: ["Produtivo", "Improdutivo"])
    CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["*"])

    @field_validator("CORS_ORIGINS", "CANDIDATE_LABELS", mode="before")
    @classmethod
    def _parse_list_env(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            s = v.strip()
            if s.startswith("["):
                try:
                    return json.loads(s)
                except Exception:
                    pass
            if s == "*":
                return ["*"]
            return [x.strip() for x in s.split(",") if x.strip()]
        return v

settings = Settings()
