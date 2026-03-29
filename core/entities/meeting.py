from dataclasses import dataclass, field
from typing import List, Optional
from core.entities.transcript import Transcript
from core.entities.speaker import SpeakerInterval

@dataclass
class MeetingData:
    transcript: Transcript
    speaker_intervals: Optional[List[SpeakerInterval]] = None
    summary_text: Optional[str] = None
    metadata: dict = field(default_factory=dict)
