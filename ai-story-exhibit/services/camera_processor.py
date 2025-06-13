# services/camera_processor.py

import tempfile
from PIL import Image
import numpy as np
from deepface import DeepFace
from services.object_sentiment import detect_objects

def analyze_camera_input(image_file_buffer) -> dict:
    """
    Given a Streamlit camera_input buffer, returns a dict with:
      - age, gender, emotion (from DeepFace)
      - objects (from YOLO via detect_objects)
    """
    # 1. Load and convert to RGB numpy array
    image = Image.open(image_file_buffer).convert("RGB")
    image_np = np.array(image)

    # 2. Save to a temp file for DeepFace
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp_path = tmp.name
        image.save(tmp_path)

    # 3. Face analysis
    face_info = {}
    try:
        result = DeepFace.analyze(
            img_path=tmp_path,
            actions=["age", "gender", "emotion"],
            enforce_detection=False
        )[0]
        face_info = {
            "age": int(result.get("age", 0)),
            "gender": result.get("gender", ""),
            "emotion": result.get("dominant_emotion", "")
        }
    except Exception:
        # on failure, return empty defaults
        face_info = {"age": None, "gender": None, "emotion": None}

    # 4. Object detection
    try:
        labels = detect_objects(image_np)
    except Exception:
        labels = []

    return {
        **face_info,
        "objects": labels
    }
