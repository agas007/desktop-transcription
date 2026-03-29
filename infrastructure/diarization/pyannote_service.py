import os
import torch
from pyannote.audio import Pipeline
from huggingface_hub import get_token

# Use environment variable to safely fetch token
class PyannoteService:
    def __init__(self):
        # Allow token from .env or fetch from `hf auth login` token cache
        self.token = os.environ.get("HUGGINGFACE_TOKEN") or get_token()
        self.pipeline = None
        if not self.token:
            print("WARNING: HUGGINGFACE_TOKEN is missing and you are not logged in via `hf auth login`. Speaker diarization will be skipped!")
            return
            
        try:
            print("Loading Pyannote Diarization 3.1 Model (First run will download ~2GB)...")
            self.pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                token=self.token
            )
            # Send to MPS (Apple Silicon GPU) if available to massively speed up!
            if self.pipeline and torch.backends.mps.is_available():
                self.pipeline.to(torch.device("mps"))
            elif self.pipeline and torch.cuda.is_available():
                self.pipeline.to(torch.device("cuda"))
        except Exception as e:
            print(f"Error loading Pyannote (Check HF Token or internet): {e}")
            self.pipeline = None

    def diarize(self, audio_path: str) -> list:
        if not self.pipeline:
            return []
            
        print("Detecting speakers using Pyannote...")
        diarization = self.pipeline(audio_path)
        
        intervals = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            intervals.append({
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker
            })
        return intervals
