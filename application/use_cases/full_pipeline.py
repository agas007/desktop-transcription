import os
from time import sleep
from infrastructure.audio.recorder import AudioRecorder
from infrastructure.audio.system_capture import SystemAudioCapture
from infrastructure.media.file_loader import FileLoader
from infrastructure.whisper.whisper_cpp import WhisperCppService
from infrastructure.llm.summarizer import OpenRouterSummarizer
from infrastructure.storage.file_writer import FileWriter
from infrastructure.diarization.pyannote_service import PyannoteService
from core.entities.meeting import MeetingData

class TranscriptionPipeline:
    def __init__(self):
        self.whisper_service = WhisperCppService()
        self.diarization_service = PyannoteService()
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
        
        # Speaker Diarization
        speaker_intervals = self.diarization_service.diarize(temp_wav)
        if speaker_intervals:
            for seg in transcript.segments:
                max_overlap = 0
                best_speaker = "UNKNOWN"
                for spk in speaker_intervals:
                    overlap = max(0, min(seg.end, spk['end']) - max(seg.start, spk['start']))
                    if overlap > max_overlap:
                        max_overlap = overlap
                        best_speaker = spk["speaker"]
                seg.speaker = best_speaker
                
        # Format the text with speaker tags for the summarizer and writer
        formatted_text = ""
        for seg in transcript.segments:
            speaker_tag = f"[{seg.speaker}] " if seg.speaker != "UNKNOWN" else ""
            formatted_text += f"[{seg.start:.2f}s - {seg.end:.2f}s] {speaker_tag}{seg.text}\n"
        
        # update transcript text so downstream tools receive the speaker-annotated version
        transcript.text = formatted_text
        
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
