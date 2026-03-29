import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    WHISPER_MODEL_PATH = os.getenv("WHISPER_MODEL_PATH", "models/whisper/ggml-small.bin")
    
    # Sound Devices
    MIC_DEVICE_INDEX = os.getenv("MIC_DEVICE_INDEX")
    SYSTEM_AUDIO_DEVICE_INDEX = os.getenv("SYSTEM_AUDIO_DEVICE_INDEX")
    
    # Audio formatting settings
    SAMPLE_RATE = 16000
    CHANNELS = 1
    
    # Outputs Folder
    OUTPUT_FOLDER_BASE = "output/meetings"
