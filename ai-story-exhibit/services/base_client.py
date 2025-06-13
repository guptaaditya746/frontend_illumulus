# services/base_client.py

from abc import ABC, abstractmethod
from typing import Any, List

class BaseClient(ABC):
    """Abstract base for all AI service clients."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        **kwargs: Any
    ) -> Any:
        """
        Generate output from a prompt.
        Returns a backend‐specific result (e.g. bytes for audio, PIL.Image for image, str for text).
        """
        pass
