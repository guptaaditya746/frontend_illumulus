# pages/2_Story_Generator.py

import streamlit as st
from state.session import init_story_state
from services.llm_client import generate_story_paragraph

st.title("🧠 Story Generator")
init_story_state()

story = st.session_state.story
prompt = story.get("prompt", "")
genre = story.get("genre", "")
elements = story.get("elements", [])
paragraphs = story.get("paragraphs", [])

# Generate paragraph if not already generated
if not paragraphs:
    with st.spinner("Generating your story..."):
        para = generate_story_paragraph(prompt, genre, elements)
        story["paragraphs"].append(para)

# Show current story
st.markdown("### 📖 Your Story So Far")
for idx, p in enumerate(story["paragraphs"]):
    st.markdown(f"**Scene {idx+1}:** {p}")

# Actions
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Regenerate Last"):
        story["paragraphs"][-1] = generate_story_paragraph(prompt, genre, elements, story["paragraphs"][:-1])

with col2:
    if st.button("➕ Add My Line"):
        user_line = st.text_input("Write your own continuation:")
        if user_line:
            story["paragraphs"].append(user_line)

with col3:
    if st.button("⏭️ Continue Story"):
        next_para = generate_story_paragraph(prompt, genre, elements, story["paragraphs"])
        story["paragraphs"].append(next_para)

# Navigation
if st.button("Next: Visualize Scene"):
    st.switch_page("pages/3_Visualize_Scene.py")
