# pages/1_Story_Builder.py

import streamlit as st
from state.session import init_story_state

st.title(" Illumulus 2025")
st.markdown("Craft your story seed using different inputs.")

init_story_state()

# Collect user input
prompt = st.text_area(" What's your story idea?", st.session_state.story.get("prompt", ""))
genre = st.selectbox(" Choose a genre", ["Fantasy", "Mystery", "Sci-Fi", "Comedy"], index=0)
# TODO: Add the idea of using different frameworks for story generation, like "Hero's Journey" or "Three Act Structure", for this different workfow of agents should should be constrcuted , maybe 20 agnets , and each framework include few agents that work together to generate the story seed.
# For now, we just use a multiselect for elements
elements = st.multiselect(" Elements to include", ["Robot", "Forest", "Dragon", "Secret", "Friendship", "Magic", "Villain"])

if st.button("   Save & Continue"):
    st.session_state.story["prompt"] = prompt
    st.session_state.story["genre"] = genre
    st.session_state.story["elements"] = elements

    st.success("Story seed saved!")
    st.switch_page("pages/2_Story_Generator.py")
