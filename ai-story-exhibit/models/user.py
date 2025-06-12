from typing import Optional, List, Any
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    """
    Represents the user's profile data captured from camera analysis.
    """
    age: Optional[int] = Field(default=None, ge=0, le=120, description="Estimated age of the user.")
    gender: Optional[str] = Field(default=None, description="Estimated gender of the user.")
    emotion: Optional[str] = Field(default=None, description="Dominant emotion detected.")
    objects: List[str] = Field(default_factory=list, description="Objects detected in the user's surroundings.")

    # If you expect other dynamic fields from camera_processor not explicitly defined,
    # you can allow extra fields, though it's often better to define them if known.
    # class Config:
    #     extra = "allow"