# db/feedback_db.py

import sqlite3
import json
import os
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator

# Path to SQLite DB (will be created on first run)
DB_PATH = os.path.join(os.path.dirname(__file__), "feedback.db")

# --- Pydantic Models for Data Validation and Structure ---

class UserProfileInFeedback(BaseModel):
    """Represents the user profile structure for feedback."""
    age: Optional[int] = None
    gender: Optional[str] = None
    emotion: Optional[str] = None
    objects: List[str] = []
    class Config:
        extra = "allow" # Allows other fields if user_profile dict has more

class StoryInFeedback(BaseModel):
    """Represents the story structure for feedback."""
    prompt: Optional[str] = ""
    genre: Optional[str] = ""
    elements: List[str] = []
    paragraphs: List[str] = []
    images: List[Any] = [] # Note: Content must be JSON-serializable (e.g., paths, base64)
    audio: List[Any] = []  # Note: Content must be JSON-serializable
    class Config:
        extra = "allow" # Allows other fields if story dict has more

class FeedbackCreate(BaseModel):
    """Model for creating a new feedback entry."""
    user_profile: UserProfileInFeedback
    story: StoryInFeedback
    rating: int = Field(..., ge=1, le=5, description="User rating from 1 to 5")
    comments: Optional[str] = None

    @field_validator('user_profile', 'story', mode='before')
    @classmethod
    def ensure_dict_input(cls, v: Any) -> Dict[str, Any]:
        """Ensures that user_profile and story inputs are dicts for parsing."""
        if not isinstance(v, dict):
            return {} # Default to empty dict if not a dict (e.g. if None was passed)
        return v

def init_db():
    """
    Initialize the SQLite database and create the feedback table if it doesn't exist.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_profile TEXT NOT NULL,
                story TEXT NOT NULL,
                rating INTEGER NOT NULL,
                comments TEXT
            )
        """)
        conn.commit()

def save_feedback(user_profile: dict, story: dict, rating: int, comments: str):
    """
    Save a feedback entry with timestamp, serialized profile & story.
    """
    try:
        feedback_data = FeedbackCreate(
            user_profile=user_profile, # Pydantic will parse this dict
            story=story,               # Pydantic will parse this dict
            rating=rating,
            comments=comments
        )
    except Exception as e: # Catches Pydantic's ValidationError
        # Handle validation error, e.g., log it or raise a custom app exception
        print(f"Error validating feedback data: {e}")
        # Depending on desired behavior, you might re-raise or return an error indicator
        raise # Re-raise the validation error to make the caller aware

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO feedback (timestamp, user_profile, story, rating, comments)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now(timezone.utc).isoformat(),
            feedback_data.user_profile.model_dump_json(),
            feedback_data.story.model_dump_json(),
            feedback_data.rating,
            feedback_data.comments
        ))
        conn.commit()
