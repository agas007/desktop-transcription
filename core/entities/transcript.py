from dataclasses import dataclass
from typing import List

@dataclass
class Segment:
    start: float
    end: float
    text: str

@dataclass
class Transcript:
    text: str
    segments: List[Segment]
