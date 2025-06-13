# pages/6_About_or_Settings.py

import streamlit as st
from datetime import datetime

st.set_page_config(page_title="About & Settings", layout="centered")
st.title("⚙️ About & Settings")

# Initialize settings in session state
if "settings" not in st.session_state:
    st.session_state.settings = {
        "llm_backend": "mock",
        "image_backend": "mock",
        "tts_backend": "mock",
        "llm_temperature": 0.7,
        "llm_max_tokens": 150,
        "image_style": "Default",
        "tts_lang": "en"
    }

# --- About Section ---
with st.expander("ℹ️ About this Exhibit", expanded=True):
    st.markdown(
        """
        **AI Story Exhibit** is an interactive experience that lets you co-create
        multimodal stories with cutting-edge AI models.

        **Features**  
        - Text-to-Story via LLM  
        - Scene illustrations via Image-Gen  
        - Dynamic narration via TTS  
        - Real-time camera & voice onboarding  
        - Branching narrative, feedback capture, and more!

        **Version:** 1.0.0  
        **Last updated:** {}
        
        ---
        """.format(datetime.utcnow().strftime("%Y-%m-%d"))
    )
    st.markdown("**Project Home:** [GitHub Repository](https://github.com/your-org/ai-story-exhibit)")
    st.markdown("**Author:** Your Name / Your Team")

# --- Settings Section ---
st.header("🔧 Settings")
settings = st.session_state.settings

# LLM Backend & Params
col1, col2 = st.columns(2)
with col1:
    st.subheader("📝 LLM Configuration")
    settings["llm_backend"] = st.selectbox(
        "LLM Backend", ["mock", "openai", "local","api"], index=["mock", "openai", "local","api"].index(settings["llm_backend"]), key="llm_backend_select"
    )
    settings["llm_temperature"] = st.slider(
        "LLM Temperature", min_value=0.0, max_value=1.0, value=settings["llm_temperature"], step=0.05, key="llm_temp_slider"
    )
    settings["llm_max_tokens"] = st.number_input(
        "LLM Max Tokens", min_value=50, max_value=1024, value=settings["llm_max_tokens"], step=50, key="llm_tokens_input"
    )

# Image Generation Backend & Style
with col2:
    st.subheader(" Image Generation")
    settings["image_backend"] = st.selectbox(
        "Image Backend", ["mock", "stable_diffusion", "huggingface","webis"],
        index=["mock", "stable_diffusion", "huggingface","webis"].index(settings["image_backend"]), key="image_backend_select"
    )
    settings["image_style"] = st.selectbox(
        "Image Art Style", ["Default", "Watercolor", "Pixel Art", "Noir"], index=["Default", "Watercolor", "Pixel Art", "Noir"].index(settings["image_style"]), key="image_style_select"
    )

# TTS Backend & Language
st.divider() # Add a visual separator

col3, col4 = st.columns(2)
with col3:
    st.subheader("🔊 Text-to-Speech")
    settings["tts_backend"] = st.selectbox(
        "TTS Backend", ["mock", "gtts", "coqui"],
        index=["mock", "gtts", "coqui"].index(settings["tts_backend"]), key="tts_backend_select"
    )
    settings["tts_lang"] = st.selectbox(
        "TTS Language", ["en", "de", "es", "fr"], index=["en","de","es","fr"].index(settings["tts_lang"]), key="tts_lang_select"
    )

# Save button
if st.button("💾 Save Settings"):
    st.session_state.settings = settings
    st.success("Settings saved! They will apply across the app.")

st.markdown("---")
st.markdown("Navigate back to any page to see these settings in action.")
