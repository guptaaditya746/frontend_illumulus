# pages/2_Story_Generator.py

import streamlit as st
from state.session import init_story_state
from services.llm_client import create_llm_client
from models.settings import AppSettings # Import AppSettings
from models.story import Story # Import Story model
from pydantic import ValidationError

st.title("Story Generator") # Added emoji for consistency
settings = st.session_state.get["settings"]

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

# Initialize LLM client using application settings
# Ensure API keys or other secrets are handled appropriately for non-mock backends
try:
    # llm = create_llm_client(
    #     backend=app_settings.llm_backend,
    #     # api_key=st.secrets.get("openai_api_key"), # Example for OpenAI, ensure secrets are configured
    #     temperature=app_settings.llm_temperature,
    #     max_tokens=app_settings.llm_max_tokens
    # )
    # Create LLM client using backend defined in settings
    llm = create_llm_client(
    settings.get("llm_backend", "mock"),
    config_path="configs/api_config.yml"  # adjust path if needed
    )

except ValueError as e:
    st.error(f"Failed to initialize LLM client: {e}")
    st.info("Please check your LLM backend configuration in the Settings page.")
    if st.button("Go to Settings"):
        st.switch_page("pages/6_About_or_Settings.py")
    st.stop()
except Exception as e: # Catch any other unexpected errors during client creation
    st.error(f"An unexpected error occurred while setting up the LLM: {e}")
    st.stop()

# --- Story Generation Logic ---
# Generate initial paragraph if not already generated
if not story_model.paragraphs:
    if story_model.prompt: # Only generate if there's a prompt
        with st.spinner("Generating your story's first paragraph..."):
            try:
                first_para = llm.generate(
                    prompt=story_model.prompt,
                    genre=story_model.genre,
                    elements=story_model.elements
                )
                story_model.paragraphs.append(first_para)
                st.session_state.story = story_model.model_dump() # Save update
                st.experimental_rerun() # Rerun to display the new paragraph
            except Exception as e:
                st.error(f"Failed to generate story: {e}")
    else:
        st.info("Please provide a story idea in the Story Builder to begin.")
        if st.button("← Go to Story Builder"):
            st.switch_page("pages/1_Story_Builder.py")
        st.stop()

# --- Display Current Story ---
st.markdown("###  Your Story So Far")
if not story_model.paragraphs:
    st.caption("Your story will appear here once generated.")
else:
    for idx, p_text in enumerate(story_model.paragraphs):
        st.markdown(f"**Scene {idx+1}:** {p_text}")

# --- Story Actions ---
if story_model.paragraphs: # Only show actions if there's content
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(" Regenerate Last"):
            if story_model.paragraphs:
                with st.spinner("Regenerating last paragraph..."):
                    try:
                        regenerated_para = llm.generate(
                            prompt=story_model.prompt, # Or a modified prompt for regeneration
                            genre=story_model.genre,
                            elements=story_model.elements
                            # context_to_change=story_model.paragraphs[-1] # Example kwarg for future LLMs
                        )
                        story_model.paragraphs[-1] = regenerated_para
                        st.session_state.story = story_model.model_dump()
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Failed to regenerate: {e}")

    with col2:
        with st.form("add_line_form", clear_on_submit=True):
            user_line = st.text_input("Write your own continuation:", key="user_story_line_input")
            submitted = st.form_submit_button("➕ Add My Line")
            if submitted and user_line:
                story_model.paragraphs.append(user_line.strip())
                st.session_state.story = story_model.model_dump()
                st.experimental_rerun() # Rerun to show the new line and clear form

    with col3:
        if st.button(" Continue Story (AI)"): # Changed button text for clarity
            with st.spinner("AI is continuing the story..."):
                try:
                    next_para = llm.generate(
                        prompt=story_model.prompt, # Or a prompt indicating continuation
                        genre=story_model.genre,
                        elements=story_model.elements,
                        story_history=story_model.paragraphs # Example kwarg for context for future LLMs
                    )
                    story_model.paragraphs.append(next_para)
                    st.session_state.story = story_model.model_dump()
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Failed to continue story: {e}")

# --- Navigation ---
# Only allow proceeding if there's at least one paragraph
if story_model.paragraphs:
    if st.button("Next: Visualize Scene"): # Added emoji
        st.switch_page("pages/3_Visualize_Scene.py")

if st.button("← Back to Story Builder"):
    st.switch_page("pages/1_Story_Builder.py")