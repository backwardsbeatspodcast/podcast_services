# AI Services

This module provides AI-powered services for the podcast automation pipeline, specifically focusing on automated transcription.

## Features

- **Episode Transcription**: Leverages OpenAI's Whisper model to convert podcast audio into text.
- **Flexible Path Handling**: Supports direct paths to media files and optional custom output directories.
- **Automatic Naming**: Automatically handles episode numbering and padding (e.g., `001.txt`) for consistent filing.

## Dependencies

- `openai-whisper`: The core transcription engine.
- `pydub`: Used for audio preprocessing and manipulation.
- `torch`: Required by Whisper for model execution.

## Usage

The primary component is the `EpisodeTranscriber` class.

### Basic Transcription

```python
from ai_services import EpisodeTranscriber

# Initialize with a specific model size ("tiny", "base", "small", "medium", "large")
transcriber = EpisodeTranscriber(model_size="base")

# Transcribe an episode
# The transcription will be saved as '001.txt' in the same folder as the MP3
transcriber.transcribe_episode(
    audio_file_path="path/to/episodes/Episode 001.mp3",
    episode_number=1
)
```

### Custom Output Folder

```python
# Transcribe and save to a specific directory
transcriber.transcribe_episode(
    audio_file_path="raw_audio.mp3",
    episode_number=42,
    output_folder="./transcripts"
)
```

## Model Sizes

Whisper offers several model sizes to balance speed and accuracy:

| Size | Parameters | English-only | Multilingual | Speed |
| :--- | :--- | :--- | :--- | :--- |
| **tiny** | 39 M | `tiny.en` | `tiny` | ~32x |
| **base** | 74 M | `base.en` | `base` | ~16x |
| **small** | 244 M | `small.en` | `small` | ~6x |
| **medium** | 769 M | `medium.en` | `medium` | ~2x |
| **large** | 1550 M | N/A | `large` | 1x |

By default, this service uses the `base` model.
