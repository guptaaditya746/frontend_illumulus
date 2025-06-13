# services/llm_client.py

from services.base_client import BaseClient
from modules.clients.llm_client import LLMClient as APIClient

class MockLLMClient(BaseClient):
    """
    A mock LLM that echoes back the prompt plus a canned ending.
    """
    def generate(self, prompt: str, **kwargs) -> str:
        genre = kwargs.get("genre", "")
        elements = kwargs.get("elements", [])
        seed = f"{prompt}. Genre: {genre}. Elements: {', '.join(elements)}."
        return f"{seed} And so, this story begins…"

class APIBaseClient(BaseClient):
    """
    Adapter for the real LLM API client defined in modules/clients/llm_client.py
    """
    def __init__(self, config_path: str = None):
        # Initialize the thin API wrapper
        self.client = APIClient(config_path=config_path)

    def generate(self, prompt: str, **kwargs) -> str:
        # Build messages for chat-based LLM API
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        # Pass through generation overrides
        return self.client.send(
            messages=messages,
            stream=kwargs.get("stream"),
            max_tokens=kwargs.get("max_tokens"),
            temperature=kwargs.get("temperature"),
            top_p=kwargs.get("top_p"),
            frequency_penalty=kwargs.get("frequency_penalty"),
            presence_penalty=kwargs.get("presence_penalty"),
            agent_name=kwargs.get("agent_name", "streamlit_app")
        )


def create_llm_client(backend: str = "mock", **kwargs) -> BaseClient:
    """
    Factory for LLM clients.
    backend: "mock" | "api"
    """
    if backend == "mock":
        return MockLLMClient()
    elif backend == "api":
        return APIBaseClient(config_path=kwargs.get("config_path"))
    else:
        raise ValueError(f"Unknown LLM backend: {backend}")
