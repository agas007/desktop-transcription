from typing import Protocol, List
from core.entities.speaker import SpeakerInterval

class DiarizationService(Protocol):
    def diarize(self, audio_path: str) -> List[SpeakerInterval]:
        """Diarize audio returning speaker intervals."""
        pass
