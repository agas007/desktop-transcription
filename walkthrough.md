# Desktop Transcription System - Walkthrough

All files for the Desktop Transcription MVP have been created and structured according to Clean Architecture in the `/Users/agas/code/desktop-transcription/` folder.

## Architecture Highlights
- **Core Entities & Protocols**: Defined basic entities (`MeetingData`, `Transcript`, `Segment`) and interface services inside `core/entities/` and `core/services/` to act as the primary abstraction layers.
- **Microphone & System Audio Recording (`infrastructure/audio/`)**: Implemented simple recording hooks using `sounddevice` and `numpy`.
- **FFmpeg Conversion (`infrastructure/media/`)**: Implemented wrapper that accepts MP4, M4A, etc., and converts them to 16kHz mono `.wav` output for correct interaction with Whisper.
- **Whisper Integration (`infrastructure/whisper/`)**: Used `whisper-cpp-python` for local transcription of `.wav` files and mapped them back into segment arrays.
- **Extensible File Outputs (`infrastructure/storage/`)**: Wrote a custom storage pipeline that parses our `MeetingData` entity into:
  - `transcript.txt` & `transcript.docx`
  - `summary.txt` & `summary.docx`
  - `raw.json`
- **LLM Summary Support (`infrastructure/llm/`)**: Created `OpenRouterSummarizer`, taking in standard API keys dynamically.
- **CLI Subparsers (`interfaces/cli/`)**: Provided user-facing endpoints (`record-mic`, `record-system`, `process`, and `full-run`).

## Next Steps for the User

> [!IMPORTANT]
> The Python code serves as a solid MVP but cannot run successfully without system environment integrations. You will need to setup the virtual environment and APIs.

1. Create a `venv` inside the folder and `pip install -r requirements.txt`.
2. Follow `README.md` instructions to install external requirements (like Mac BlackHole or Windows WASAPI driver rules), and install standard `ffmpeg`.
3. Provide an OpenRouter API key and Whisper model binary path in `.env`.
4. Test the pipeline via `python main.py record-mic` command!
