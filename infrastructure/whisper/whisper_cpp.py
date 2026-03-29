from whisper_cpp_python import Whisper
from core.entities.transcript import Transcript, Segment
from core.services.transcription_service import TranscriptionService
from app.config import Config
import os

class WhisperCppService(TranscriptionService):
    def __init__(self):
        self.model_path = Config.WHISPER_MODEL_PATH
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Whisper model not found at {self.model_path}. Please download it.")
        self.whisper = Whisper(model_path=self.model_path)

    def transcribe(self, audio_path: str) -> Transcript:
        # whisper-cpp-python process requires the file or numpy array
        # Assuming we just pass the wrapper
        result = self.whisper.transcribe(audio_path)
        
        segments = []
        full_text = []
        for segment in result.get("segments", []):
            start = float(segment.get("start", 0.0))
            end = float(segment.get("end", 0.0))
            text = segment.get("text", "")
            segments.append(Segment(start=start, end=end, text=text))
            full_text.append(text)
            
        return Transcript(text=" ".join(full_text), segments=segments)
