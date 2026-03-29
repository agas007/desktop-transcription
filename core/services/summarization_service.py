from typing import Protocol
from core.entities.transcript import Transcript

class SummarizationService(Protocol):
    def summarize(self, transcript: Transcript) -> str:
        """Generate a structured summary of the meeting."""
        pass
