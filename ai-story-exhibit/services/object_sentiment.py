# services/object_sentiment.py

from ultralytics import YOLO
from transformers import pipeline

# Load models once at import time
_yolo_model = YOLO("yolov8n.pt")  # requires ultralytics + torch
_sentiment_pipe = pipeline("sentiment-analysis")  # requires transformers + torch

def detect_objects(image_np: "np.ndarray") -> list:
    """
    Run YOLO object detection on an image (numpy array).
    Returns a deduplicated list of object class names.
    """
    results = _yolo_model(image_np)
    labels = [box.name for box in results[0].boxes]
    # dedupe and return
    return list(set(labels))

def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment of a given text.
    Returns a dict with:
      - label: 'POSITIVE' or 'NEGATIVE' (or labels from the model)
      - score: confidence float
    """
    res = _sentiment_pipe(text, truncation=True)[0]
    return {
        "label": res["label"],
        "score": float(res["score"])
    }
