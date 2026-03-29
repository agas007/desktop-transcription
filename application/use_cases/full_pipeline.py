import os
from time import sleep
from infrastructure.audio.recorder import AudioRecorder
from infrastructure.audio.system_capture import SystemAudioCapture
from infrastructure.media.file_loader import FileLoader
from infrastructure.whisper.whisper_cpp import WhisperCppService
from infrastructure.llm.summarizer import OpenRouterSummarizer
from infrastructure.storage.file_writer import FileWriter
from core.entities.meeting import MeetingData

class TranscriptionPipeline:
    def __init__(self):
        self.whisper_service = WhisperCppService()
        self.summarization_service = OpenRouterSummarizer()
        self.file_writer = FileWriter()
        self.file_loader = FileLoader()

    def record_microphone(self, duration: int = None):
        print("Starting microphone recording. Press Ctrl+C to stop manually.")
        recorder = AudioRecorder()
        temp_wav = "temp_mic.wav"
        recorder.start()
        try:
            if duration:
                sleep(duration)
            else:
                while True:
                    sleep(0.1)
        except KeyboardInterrupt:
            print("\nRecording stopped by user.")
            
        path = recorder.stop(temp_wav)
        if path:
            return self.process_file(path)

    def record_system(self, duration: int = None):
        print("Starting system audio recording. Press Ctrl+C to stop manually.")
        recorder = SystemAudioCapture()
        temp_wav = "temp_system.wav"
        recorder.start()
        try:
            if duration:
                sleep(duration)
            else:
                while True:
                    sleep(0.1)
        except KeyboardInterrupt:
            print("\nRecording stopped by user.")
            
        path = recorder.stop(temp_wav)
        if path:
            return self.process_file(path)

    def process_file(self, file_path: str):
        print(f"Processing audio from {file_path}")
        temp_wav = "temp_converted.wav"
        self.file_loader.load_and_convert(file_path, temp_wav)
        
        print("Starting transcription with local whisper.cpp...")
        transcript = self.whisper_service.transcribe(temp_wav)
        
        print("Generating meeting summary...")
        summary = self.summarization_service.summarize(transcript)

        meeting = MeetingData(
            transcript=transcript,
            summary_text=summary
        )

        print("Writing outputs...")
        output_folder = self.file_writer.write(meeting)
        
        print(f"Processing complete! Results saved to: {output_folder}")
        
        # Cleanup temp
        if os.path.exists(temp_wav):
            os.remove(temp_wav)
            
        return output_folder
