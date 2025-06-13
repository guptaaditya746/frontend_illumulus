# state/session.py

import streamlit as st

# Import your Pydantic models
from models.story import Story
from models.user import UserProfile
from models.settings import AppSettings

def init_app_state():
    """
    Initialize all session state variables for the app:
      - story: holds story seed and generated content
      - user_profile: holds camera & voice analysis results
      - settings: holds user-configurable backend & parameters
    Call this at the start of every page.
    """
    # Story state
    if 'story' not in st.session_state:
        st.session_state['story'] = Story().model_dump()

    # User profile from onboarding (camera/voice)
    if 'user_profile' not in st.session_state:
        # UserProfile might be partially filled or empty initially
        st.session_state['user_profile'] = UserProfile().model_dump()

    # App settings (backends, model params)
    if 'settings' not in st.session_state:
        st.session_state['settings'] = AppSettings().model_dump()

# Convenience aliases for backward compatibility
init_story_state = init_app_state
init_user_profile = init_app_state
init_settings = init_app_state
