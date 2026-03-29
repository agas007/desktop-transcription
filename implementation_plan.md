# Actionable Desktop Transcription MVP

Implementing a local-first transcription system utilizing Clean Architecture in Python, supporting 3 modes (Microphone, System Audio, File).

## User Review Required

> [!WARNING]
> Please verify the project directory. I plan to create the new project in `/Users/agas/code/desktop-transcription/`. Let me know if you would prefer a different location.

> [!IMPORTANT]
> The system requires BlackHole on Mac for system audio recording, and `ffmpeg` installed for media file conversion. The Whisper.cpp setup and specific path to the model will need to be configured via the `.env` file. These dependencies must be installed on your host system before the script can run fully correctly.

## Proposed Changes

We will generate the folder layout and place the files exactly as instructed:

### Configuration and Infrastructure
- `requirements.txt`: Set up dependencies (`sounddevice`, `numpy`, `ffmpeg-python`, `torch`, `python-dotenv`, `python-docx`, `pyannote.audio` if doing diarization).
- `.env`: API keys (if summarizing via LLM), model paths.
- `app/config.py`: Load settings from env.

### Core Architecture (Clean Architecture)
- `core/entities/*`: Base models (Transcript, Speaker, Meeting).
- `core/services/*`: Abstract definitions/business logic for Transcription, Diarization, and Summarization.

### Infrastructure Layer (External Tools)
- `infrastructure/audio/*`: Python bindings to record `.wav` from mic and system loopbacks.
- `infrastructure/media/*`: Wrap `ffmpeg-python` to resample/extract audio.
- `infrastructure/whisper/whisper_cpp.py`: Interface with `whisper-cpp-python` binding.
- `infrastructure/llm/summarizer.py`: Call OpenRouter via `openai` python package.
- `infrastructure/storage/*`: File writers for `.txt`, `.json`, and `.docx` using `python-docx`.

### Application Use Cases & CLI
- `application/use_cases/*`: Tie it all together parsing from mic vs system vs file -> standard WAV -> Whisper -> Prompt -> Storage.
- `interfaces/cli/cli.py`: Implement standard endpoints via `argparse` or `click`.

## Open Questions

> [!NOTE]
> 1. We will use **OpenRouter** for the LLM summarization. This will be implemented using the `openai` python package pointing to the OpenRouter base URL.
> 2. For `whisper.cpp`, we will use the `whisper-cpp-python` binding to keep inference fully wrapped in Python rather than calling shell commands.

## Verification Plan

### Automated Tests
- We will rely on manual testing and basic CLI validation first due to complexity of actual audio hardware loops.

### Manual Verification
- Run `python main.py record-mic` to generate short recording.
- Run `python main.py process --file <sample>` to test the file pipeline.

