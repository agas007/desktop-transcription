import ffmpeg
import os
from app.config import Config

class FileLoader:
    def __init__(self):
        self.sample_rate = Config.SAMPLE_RATE
        self.channels = Config.CHANNELS

    def load_and_convert(self, input_path: str, output_path: str) -> str:
        """
        Converts the input file (mp4, m4a, wav, etc.) into a 16kHz mono WAV file.
        Returns the output path.
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        try:
            (
                ffmpeg.input(input_path)
                .output(output_path, ac=self.channels, ar=self.sample_rate, format='wav')
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            return output_path
        except ffmpeg.Error as e:
            print(f"FFmpeg error: {e.stderr.decode('utf-8')}")
            raise e
