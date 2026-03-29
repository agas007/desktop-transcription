# Setup System

- [x] Create project folder `desktop-transcription` and subdirectories.
- [x] Create `requirements.txt` and `.env`.

# Core Architecture & Config

- [x] Implement `app/config.py`
- [x] Implement `core/entities` (Transcript, Speaker, Meeting)
- [x] Implement `core/services` interfaces

# Infrastructure Layer

- [x] Implement `infrastructure/audio/recorder.py` and `system_capture.py`
- [x] Implement `infrastructure/media/file_loader.py`
- [x] Implement `infrastructure/whisper/whisper_cpp.py`
- [x] Implement `infrastructure/llm/summarizer.py`
- [x] Implement `infrastructure/storage/file_writer.py`

# App Layer & CLI

- [x] Implement `application/use_cases/` pipelines
- [x] Implement `interfaces/cli/cli.py`
- [x] Implement `main.py`
- [x] Write `README.md` and verify.
