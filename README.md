# Desktop Transcription MVP

A local-first transcription system utilizing Clean Architecture in Python.

## Prerequisites & Setup

1. **Install System Dependencies**
   - **FFmpeg**: Required to convert audio files to 16kHz WAV format.
     - Mac: `brew install ffmpeg`
     - Windows: Install via `winget install ffmpeg` or download binaries.
   - **Virtual Audio Cable (for System Audio)**
     - Mac: Install [BlackHole](https://existential.audio/blackhole/) (`brew install blackhole-2ch`).
     - Windows: Stereo Mix or WASAPI Loopback works based on device selection.

2. **Project Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Models & API Keys**
   - Create a `.env` file based on the provided defaults.
   - **Whisper**: Download a `ggml` whisper model (e.g. `ggml-base.en.bin`) and place it inside `models/whisper/`, or configure the `WHISPER_MODEL_PATH` in `.env`.
   - **OpenRouter**: To generate Meeting Summary, add your OpenRouter API key inside the `.env` file `OPENROUTER_API_KEY=xxx`.

## Usage Examples

**1. Microphone Input**
Record from mic until you press `Ctrl+C`, then the system will generate the transcript and summary.
```bash
python main.py record-mic
```

**2. System Audio Input**
Record output from the system (requires routing system output to an input device like BlackHole).
```bash
python main.py record-system
```

**3. Existing File**
Transcribe and summarize an existing MP4, M4A, or WAV file.
```bash
python main.py process --file input/recordings/meeting.mp4
```

**4. Outputs**
Outputs will be generated inside: `output/meetings/YYYY-MM-DD_HH-MM-SS/`
- `transcript.txt` and `transcript.docx`
- `summary.txt` and `summary.docx`
- `raw.json`
