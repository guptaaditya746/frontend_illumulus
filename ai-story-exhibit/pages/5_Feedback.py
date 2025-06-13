# pages/5_Feedback.py

import streamlit as st
from state.session import init_story_state
from db.feedback_db import save_feedback

st.title("📝 Feedback")
st.markdown("We’d love to hear about your experience!")

init_story_state()
story = st.session_state.story
profile = st.session_state.get("user_profile", {})

# If no story generated, redirect back
if not story.get("paragraphs"):
    st.warning("No story found. Please start from the beginning.")
    if st.button("← Back to Home"):
        st.switch_page("main")
    st.stop()

# Show the full story recap
st.markdown("### Your Story Recap")
for idx, p in enumerate(story["paragraphs"]):
    st.markdown(f"**Scene {idx+1}:** {p}")

st.markdown("### Your Feedback")

rating = st.slider("★ How much did you enjoy it?", 1, 5, 5)
comments = st.text_area("Any comments or suggestions?")

if st.button("Submit Feedback"):
    save_feedback(profile, story, rating, comments)
    st.success("Thank you! Your feedback has been recorded.")
    st.markdown("Feel free to restart and create another story:")
    if st.button("🎉 Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
