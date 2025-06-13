# services/tts_client.py

import io
import torch
from gtts import gTTS
from TTS.api import TTS as CoquiTTS
from typing import Any
from services.base_client import BaseClient
import numpy as np
import soundfile as sf

try:
    from nltk.tokenize import sent_tokenize
except ImportError:
    print("NLTK not found. Please install it for sentence tokenization: pip install nltk")
    print("Also, download the 'punkt' tokenizer: python -m nltk.downloader punkt")

class GTTSTTSClient(BaseClient):
    """Adapter for gTTS (Google)."""
    def generate(self, prompt: str, **kwargs: Any) -> bytes:
        tts = gTTS(text=prompt, lang=kwargs.get("lang", "en"))
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()  # raw MP3 bytes

class CoquiTTSClient(BaseClient):
    """Adapter for Coqui TTS."""
    def __init__(self, model_name: str, speaker: str = None, speaker_wav: str = None):
        # move to GPU if available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = CoquiTTS(model_name).to(device)
        self.speaker = speaker
        self.speaker_wav = speaker_wav

    def generate(self, prompt: str, **kwargs: Any) -> bytes:
        """
        Generates audio from text. If the text is long, it splits it into sentences
        and synthesizes each sentence, then concatenates the audio.
        """
        try:
            sentences = sent_tokenize(prompt)
        except NameError: # nltk or sent_tokenize not available
            # Fallback: treat the whole prompt as one sentence if nltk fails
            print("Warning: NLTK sentence tokenizer not available. Processing text as a single chunk.")
            sentences = [prompt]
        except Exception as e:
            print(f"Error during sentence tokenization: {e}. Processing text as a single chunk.")
            sentences = [prompt]

        all_audio_segments = []
        for sentence in sentences:
            if not sentence.strip():
                continue
            # Generate audio for each sentence
            wav_segment_np = self.tts.tts(
                text=sentence,
                speaker_wav=kwargs.get("speaker_wav", self.speaker_wav),
                speaker=kwargs.get("speaker", self.speaker),
                language=kwargs.get("language", "en") # Coqui TTS uses 'language'
            )
            all_audio_segments.append(np.array(wav_segment_np))

        if not all_audio_segments:
            return b'' # Return empty bytes if no audio was generated

        concatenated_audio_np = np.concatenate(all_audio_segments)
        buf = io.BytesIO()
        sf.write(buf, concatenated_audio_np, samplerate=self.tts.sampling_rate, format="WAV")
        buf.seek(0)
        return buf.read()

def create_tts_client(backend: str, **kwargs) -> BaseClient:
    """
    Factory for TTS clients.
    backend: "gtts" or "coqui"
    """
    if backend == "gtts":
        return GTTSTTSClient()
    elif backend == "coqui":
        return CoquiTTSClient(
            model_name=kwargs.get("model_name", "tts_models/multilingual/multi-dataset/xtts_v2"),
            speaker=kwargs.get("speaker"),
            speaker_wav=kwargs.get("speaker_wav")
        )
    else:
        raise ValueError(f"Unknown TTS backend: {backend}")
