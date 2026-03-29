import threading
import sounddevice as sd
import numpy as np
import wave
from app.config import Config

class AudioRecorder:
    def __init__(self, device_index=None):
        self.device_index = device_index
        self.sample_rate = Config.SAMPLE_RATE
        self.channels = Config.CHANNELS
        self.recording = False
        self.frames = []
        self._thread = None

    def _record(self):
        try:
            with sd.InputStream(samplerate=self.sample_rate,
                                channels=self.channels,
                                device=self.device_index,
                                dtype='int16') as stream:
                while self.recording:
                    data, overflowed = stream.read(1024)
                    if data is not None:
                        self.frames.append(data)
        except Exception as e:
            print(f"Error recording audio: {e}")

    def start(self):
        self.recording = True
        self.frames = []
        self._thread = threading.Thread(target=self._record)
        self._thread.start()

    def stop(self, output_path: str):
        self.recording = False
        if self._thread:
            self._thread.join()
        
        if self.frames:
            audio_data = np.concatenate(self.frames, axis=0)
            with wave.open(output_path, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2) # 16-bit
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio_data.tobytes())
            return output_path
        return None
