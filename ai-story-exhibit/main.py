# main.py

import streamlit as st
from state.session import init_story_state
from models.user import UserProfile # Import the Pydantic model
from pydantic import ValidationError
from services.camera_processor import analyze_camera_input

st.set_page_config(page_title="ILLUMULUS 2025", layout="centered")
st.title(" A Mutlimodel Co-Writer UNLIKE ANY OTHER")

init_story_state()  # Initialize session state for story and user profile
st.markdown("Welcome to the **ILLUMULUS 2025** exhibit! This interactive experience allows you to co-create a multimodal story with AI. Let's start by getting to know you better through your camera and voice.")
st.markdown("###  Camera Onboarding")

st.markdown("### Step 1: Let’s get to know you!")

# Show camera input
img_file_buffer = st.camera_input("Take a snapshot of yourself")

if img_file_buffer is not None:
    validated_profile: Optional[UserProfile] = None
    with st.spinner("Analyzing your image... This may take a moment."):
        try:
            # The analyze_camera_input function handles internal errors
            # and returns a dictionary with available data or defaults.
            raw_profile_data = analyze_camera_input(img_file_buffer)
            validated_profile = UserProfile.model_validate(raw_profile_data)
        except ValidationError as ve:
            st.error(f"There was an issue with the analyzed data format: {ve}")
            # Log the validation error for debugging if needed
            print(f"Pydantic ValidationError: {ve.errors()}")
        except Exception as e:
            st.error(f"An unexpected error occurred during image analysis: {e}")
## TODO : Here we can add audio interaction , check youtube for examples
  
    # Check if analysis yielded any results
    if validated_profile and \
       (validated_profile.age is not None or \
        validated_profile.gender or \
        validated_profile.emotion or \
        validated_profile.objects):
        st.success("Analysis complete!")
        # Store the Pydantic model instance or its dictionary representation
        # Storing the model instance is fine if you consistently use it.
        # Storing a dict might be simpler if other parts of the app expect dicts.
        st.session_state["user_profile"] = validated_profile.model_dump()
        st.markdown("###  Detected Info:")
        st.json(validated_profile.model_dump_json(indent=2)) # Pretty print JSON
        if st.button("Continue to Story Builder"):
            st.switch_page("pages/1_Story_Builder.py")
    else:
        st.error("Could not extract sufficient information from the image. Please try taking another picture with a clearer view of your face and any surrounding objects.")
