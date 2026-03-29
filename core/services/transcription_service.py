from typing import Protocol
from core.entities.transcript import Transcript

class TranscriptionService(Protocol):
    def transcribe(self, audio_path: str) -> Transcript:
        """Transcribe audio from a 16kHz WAV file."""
        pass
