# services/image_gen_client.py

import base64
import io
from abc import ABC
from PIL import Image, ImageDraw
from services.base_client import BaseClient
from stable_diffusion import WebisAPI  # <-- your working API

# --- Existing mock client ---
class MockImageClient(BaseClient, ABC):
    def generate(self, prompt: str, **kwargs) -> Image.Image:
        img = Image.new("RGB", (512, 512), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        text = prompt[:100] + "…" if len(prompt) > 100 else prompt
        draw.multiline_text((10, 10), text, fill=(0, 0, 0))
        return img

# --- New Webis-backed client ---
class WebisImageClient(BaseClient):
    def __init__(self):
        self.api = WebisAPI()

    def generate(self, prompt: str, **kwargs) -> Image.Image:
        # 1) Call your API to get base64 string
        b64 = self.api.generate(prompt)
        # 2) Decode & load into PIL
        img_data = base64.b64decode(b64)
        return Image.open(io.BytesIO(img_data))

# --- Factory update ---
def create_image_client(backend: str, **kwargs) -> BaseClient:
    """
    Factory for image clients.
    backend: "mock" | "webis"
    """
    if backend == "mock":
        return MockImageClient()
    elif backend == "webis":
        return WebisImageClient()
    else:
        raise ValueError(f"Unknown image backend: {backend}")
