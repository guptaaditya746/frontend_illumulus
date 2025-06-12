from typing import List, Optional, Any
from pydantic import BaseModel, Field

class Story(BaseModel):
    prompt: str = ""
    genre: str = ""
    elements: List[str] = Field(default_factory=list)
    paragraphs: List[str] = Field(default_factory=list)
    images: List[Any] = Field(default_factory=list) # Consider specific types or Base64 strings
    audio: List[Any] = Field(default_factory=list)  # Consider specific types or Base64 strings
