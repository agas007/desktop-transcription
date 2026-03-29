from infrastructure.audio.recorder import AudioRecorder
from app.config import Config

class SystemAudioCapture(AudioRecorder):
    def __init__(self):
        # Defaulting to configuring specific devices via env var.
        # Loopback mapping relies on standard `sounddevice` configurations or external loops.
        device_index = None
        if Config.SYSTEM_AUDIO_DEVICE_INDEX:
            device_index = int(Config.SYSTEM_AUDIO_DEVICE_INDEX)
        
        super().__init__(device_index=device_index)
