from typing import Literal
from pydantic import BaseModel, Field

class AppSettings(BaseModel):
    llm_backend: Literal["mock", "openai", "local"] = "mock"
    image_backend: Literal["mock", "stable_diffusion", "huggingface"] = "mock"
    tts_backend: Literal["mock", "gtts", "coqui"] = "mock"
    llm_temperature: float = Field(default=0.7, ge=0.0, le=2.0) # OpenAI allows up to 2.0
    llm_max_tokens: int = Field(default=150, ge=10)
    image_style: Literal["Default", "Watercolor", "Pixel Art", "Noir"] = "Default"
    tts_lang: Literal["en", "de", "es", "fr"] = "en"
