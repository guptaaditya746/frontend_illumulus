import streamlit as st

st.set_page_config(page_title="AI Story Exhibit", layout="centered")

st.title("Welcome to the AI Story Exhibit 🎨📖")
st.markdown("Begin your creative journey — co-create a story with AI.")

if st.button("Start Your Story"):
    st.switch_page("pages/1_Story_Builder.py")
