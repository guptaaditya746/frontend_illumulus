# pages/2_Story_Generator.py

import streamlit as st
from state.session import init_story_state

st.title("🧠 Story Generator")
init_story_state()

seed = st.session_state.story

st.markdown("**Your Prompt:**")
st.write(seed["prompt"])
st.markdown("**Genre:** " + seed["genre"])
st.markdown("**Elements:** " + ", ".join(seed["elements"]))

if st.button("Go Back"):
    st.switch_page("pages/1_Story_Builder.py")
