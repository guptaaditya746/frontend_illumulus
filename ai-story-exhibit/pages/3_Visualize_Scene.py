# pages/3_Visualize_Scene.py
# This page will:

# Read story["paragraphs"] and story["images"] from session state.

# If there’s a paragraph without an image, show a “Generate Image” button.

# Display all generated images alongside their paragraphs.

# Provide navigation to the Narration page.
import streamlit as st
from state.session import init_story_state
from models.story import Story # Import the Story Pydantic model
from services.image_gen_client import create_image_client
from models.settings import AppSettings # Import AppSettings
from pydantic import ValidationError

st.title(" Visualize Scene") # Added emoji, removed leading space
st.markdown("Generate or review visuals for each part of your story.")
init_story_state()

# Load settings, ensuring it's a validated model or a dict derived from it
try:
    app_settings = AppSettings.model_validate(st.session_state.get("settings", {}))
except ValidationError as e:
    st.error(f"Application settings are invalid: {e}. Please check the settings page.")
    if st.button("Go to Settings"):
        st.switch_page("pages/6_About_or_Settings.py")
    st.stop()

# Load story data from session state and validate with Pydantic model
try:
    story_model = Story.model_validate(st.session_state.get("story", {}))
except ValidationError as e:
    st.error(f"Story data is corrupted: {e}. Please try returning to the Story Builder.")
    if st.button("Go to Story Builder"):
        st.switch_page("pages/1_Story_Builder.py")
    st.stop()

paragraphs = story_model.paragraphs
images = story_model.images # This will be a list, images are likely PIL.Image objects

if not paragraphs:
    st.warning("No story paragraphs found. Go back to the Story Generator first.")
    if st.button("← Go to Story Generator"):
        st.switch_page("pages/2_Story_Generator.py")
    st.stop()

# For any paragraph missing an image, generate one
for idx, para in enumerate(paragraphs):
    st.markdown(f"**Scene {idx+1}:** {para}")
    if idx < len(images):
        # Assuming images[idx] is a PIL.Image object or compatible with st.image
        st.image(images[idx], caption=f"Visual for Scene {idx+1}", use_column_width=True)
    else:
        if st.button(f"Generate Image for Scene {idx+1}"):
            with st.spinner("Generating image..."):
                try:
                    image_client = create_image_client(app_settings.image_backend)
                    # NOTE: Ensure that the concrete image generation client selected via
                    # app_settings.image_backend is designed to accept and utilize the 'style' keyword argument.
                    img = image_client.generate(prompt=para, style=app_settings.image_style)
                    story_model.images.append(img) # Append to the Pydantic model's list
                    st.session_state.story = story_model.model_dump() # Save updated model back
                except Exception as e:
                    st.error(f"Image generation failed: {e}")
                    # Potentially log e for debugging
            st.experimental_rerun()
        # Stop rendering further scenes until this one has an image
        break

# If all scenes have images, let user move on
if paragraphs and len(images) == len(paragraphs): # Ensure paragraphs is not empty
    st.success("All scenes visualized!")
    if st.button("Next: Narrate Story "):
        st.switch_page("pages/4_Narrate_Story.py")

# Allow going backwards
if st.button("← Back to Story Generator"):
    st.switch_page("pages/2_Story_Generator.py")
