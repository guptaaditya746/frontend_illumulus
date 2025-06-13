# /home/prims/frontend_illumulus/ai-story-exhibit/tests/unit/test_story_model.py

import pytest
from pydantic import ValidationError
from models.story import Story # Assuming models.story is accessible

def test_story_model_creation_default():
    """Test Story model creation with default values."""
    story = Story()
    assert story.prompt == ""
    assert story.genre == ""
    assert story.elements == []
    assert story.paragraphs == []
    assert story.images == []
    assert story.audio == []

def test_story_model_creation_with_data():
    """Test Story model creation with provided data."""
    data = {
        "prompt": "A brave knight",
        "genre": "Fantasy",
        "elements": ["dragon", "castle"],
        "paragraphs": ["Once upon a time...", "He found a dragon."],
        # Assuming images and audio would be more complex objects or paths,
        # for simplicity, we'll test with empty lists or mock data if needed.
        "images": [],
        "audio": []
    }
    story = Story(**data)
    assert story.prompt == "A brave knight"
    assert story.genre == "Fantasy"
    assert story.elements == ["dragon", "castle"]
    assert story.paragraphs == ["Once upon a time...", "He found a dragon."]

def test_story_model_validation_error():
    """Test Story model validation for incorrect data types (if any strict types are enforced)."""
    # Example: If 'elements' was expected to be a list of strings, and we pass an int.
    # This depends on your Pydantic model's specific validators.
    pass # Add specific validation tests based on your model constraints.