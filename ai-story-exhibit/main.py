# main.py

import streamlit as st
import cv2
import tempfile
import numpy as np
from PIL import Image
from deepface import DeepFace
from ultralytics import YOLO
from state.session import init_story_state

st.set_page_config(page_title="AI Story Onboarding", layout="centered")
st.title("👋 Welcome to the AI Story Exhibit")

init_story_state()

st.markdown("### Step 1: Let’s get to know you!")

# Show camera input
img_file_buffer = st.camera_input("📷 Take a snapshot of yourself")

if img_file_buffer is not None:
    # Convert to image
    image = Image.open(img_file_buffer).convert("RGB")
    image_np = np.array(image)

    # Save temporarily
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        image_path = tmp.name
        image.save(image_path)

    # 1. Face Analysis (DeepFace)
    with st.spinner("Analyzing face..."):
        try:
            face_info = DeepFace.analyze(img_path=image_path, actions=["age", "gender", "emotion"], enforce_detection=False)[0]
            st.success("Face analysis complete.")
        except Exception as e:
            st.error("Face analysis failed.")
            face_info = {}

    # 2. Object Detection (YOLOv8)
    with st.spinner("Detecting objects..."):
        try:
            model = YOLO("yolov8n.pt")
            results = model(image_np)
            labels = list(set([r.name for r in results[0].boxes.data]))
            st.success("Object detection complete.")
        except Exception as e:
            st.error("Object detection failed.")
            labels = []

    # Show user profile
    user_profile = {
        "age": face_info.get("age"),
        "gender": face_info.get("gender"),
        "emotion": face_info.get("dominant_emotion"),
        "objects": labels
    }

    st.session_state["user_profile"] = user_profile

    st.markdown("### ✅ Detected Info:")
    st.json(user_profile)

    if st.button("Continue to Story Builder"):
        st.switch_page("pages/1_Story_Builder.py")
