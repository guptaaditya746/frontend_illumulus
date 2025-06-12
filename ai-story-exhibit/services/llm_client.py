# services/llm_client.py

def generate_story_paragraph(prompt: str, genre: str, elements: list, previous_paragraphs: list = []):
    """
    Mock story generation function.
    Replace this with a call to your LLM API later.
    """
    seed = f"{prompt}. Genre: {genre}. Elements: {', '.join(elements)}."
    base = " ".join(previous_paragraphs)
    return f"{base} Once upon a time, {seed.lower()} The story begins..."
