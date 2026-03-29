from dataclasses import dataclass

@dataclass
class SpeakerInterval:
    speaker_label: str
    start: float
    end: float
