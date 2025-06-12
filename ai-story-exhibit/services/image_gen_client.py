# services/image_gen_client.py
# A mock image generator that returns a placeholder PIL image. Later you can swap this out for your real image-gen API.
from PIL import Image, ImageDraw, ImageFont

def generate_image_from_text(prompt: str):
    """
    Mock image generation—returns a simple placeholder image.
    Replace with your real image-gen API call.
    """
    # Create a white canvas
    img = Image.new("RGB", (512, 512), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Draw the prompt text (truncated)
    text = (prompt[:100] + "...") if len(prompt) > 100 else prompt
    margin = 10
    draw.multiline_text((margin, margin), text, fill=(0, 0, 0))

    return img
