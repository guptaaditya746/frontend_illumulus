# state/session.py

import streamlit as st

def init_story_state():
    if 'story' not in st.session_state:
        st.session_state['story'] = {
            "prompt": "",
            "genre": "",
            "elements": [],
            "paragraphs": [],  # story grows incrementally
            "images": [],      # one image per scene
            "audio": []        # optional TTS per paragraph
        }
