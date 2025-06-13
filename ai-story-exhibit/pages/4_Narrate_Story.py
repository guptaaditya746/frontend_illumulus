from db.story_logger import save_story
# pages/4_Narrate_Story.py

import streamlit as st
from state.session import init_story_state
from services.tts_client import create_tts_client
from models.settings import AppSettings # Import AppSettings
from models.story import Story # Import Story model
from pydantic import ValidationError

st.title(" Narrate Story") # Added emoji, removed leading space
st.markdown("Listen to your story come to life!")

init_story_state()

# Load settings and story data with Pydantic validation
try:
    app_settings = AppSettings.model_validate(st.session_state.get("settings", {}))
except ValidationError as e:
    st.error(f"Application settings are invalid: {e}. Please check the settings page.")
    if st.button("Go to Settings"):
        st.switch_page("pages/6_About_or_Settings.py")
    st.stop()

try:
    story_model = Story.model_validate(st.session_state.get("story", {}))
except ValidationError as e:
    st.error(f"Story data is corrupted: {e}. Please try returning to the Story Builder.")
    if st.button("Go to Story Builder"):
        st.switch_page("pages/1_Story_Builder.py")
    st.stop()

paragraphs = story_model.paragraphs
audios = story_model.audio # This will be a list of bytes objects

if not paragraphs:
    st.warning("No story generated yet. Go back to Story Generator.")
    if st.button("← Go to Story Generator"):
        st.switch_page("pages/2_Story_Generator.py")
    st.stop()

# Initialize TTS client using application settings
try:
    tts_kwargs = {}
    if app_settings.tts_backend == "coqui":
        # Example: if you want to hardcode a speaker for Coqui or make it configurable in AppSettings
        tts_kwargs["speaker"] = "Craig Gutsy" # Or app_settings.coqui_speaker_name if defined
        # tts_kwargs["model_name"] = app_settings.coqui_model_name # If you add this to AppSettings

    tts = create_tts_client(
        backend=app_settings.tts_backend,
        **tts_kwargs
    )
except ValueError as e: # From create_tts_client for unknown backend
    st.error(f"Failed to initialize TTS client: {e}")
    st.info("Please check your TTS backend configuration in the Settings page.")
    if st.button("Go to Settings"):
        st.switch_page("pages/6_About_or_Settings.py")
    st.stop()
except Exception as e: # Catch any other unexpected errors during client creation
    st.error(f"An unexpected error occurred while setting up TTS: {e}")
    st.stop()

# For each paragraph, generate/play audio
for idx, para in enumerate(paragraphs):
    st.markdown(f"**Scene {idx+1}:** {para}")
    if idx < len(audios):
        # Coqui generates WAV, gTTS generates MP3.
        # st.audio can often infer, but explicit format can be safer if known.
        audio_format = "audio/wav" if app_settings.tts_backend == "coqui" else "audio/mpeg"
        st.audio(audios[idx], format=audio_format)
    else:
        if st.button(f" Generate Narration for Scene {idx+1}"):
            with st.spinner("Generating narration..."):
                try:
                    # Pass the language from settings to the generate method
                    audio_bytes = tts.generate(prompt=para, language=app_settings.tts_lang)
                    story_model.audio.append(audio_bytes) # Append raw bytes
                    st.session_state.story = story_model.model_dump() # Save updated model back
                except Exception as e:
                    st.error(f"Narration generation failed: {e}")
                    # Potentially log e for debugging
            st.experimental_rerun()
        # Wait until this scene has audio before showing the next
        break

# If all scenes have audio, allow moving on
if paragraphs and len(audios) == len(paragraphs): # Ensure paragraphs is not empty
    st.success("All scenes narrated!")
    if st.button("Next: Feedback 📝"):
        # Save the story before navigating to feedback
        try:
            save_story(
                st.session_state.get("user_profile", {}), # This should be a dict
                { # Construct seed from story_model
                    "prompt": story_model.prompt,
                    "genre": story_model.genre,
                    "elements": story_model.elements
                },
                story_model.paragraphs # Pass paragraphs list
            )
            st.toast("Story progress saved!", icon="💾")
        except Exception as e:
            st.error(f"Could not save story progress: {e}")
            # Decide if you still want to navigate or not
        st.switch_page("pages/5_Feedback.py")

# Navigation
if st.button("← Back to Visualize"):
    st.switch_page("pages/3_Visualize_Scene.py")
