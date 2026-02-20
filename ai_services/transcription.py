import os
import whisper
from pydub import AudioSegment  # might not be needed unless we preprocess
from typing import Optional


class EpisodeTranscriber:
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self.model = whisper.load_model(model_size)

    def transcribe_episode(self, audio_file_path: str, episode_number: int, output_folder: Optional[str] = None) -> Optional[str]:
        '''Transcribes the given audio file and saves the transcription as a text file.
        Args:     audio_file_path: Path to the audio file to transcribe.
            episode_number: The episode number for naming the output file.
            output_folder: Optional folder to save the transcription. If not provided, saves in the same directory as the audio file.
        Returns:    The path to the saved transcription text file, or None if transcription failed.
        ''':

        if not os.path.exists(audio_file_path):
            print(f"[EpisodeTranscriber] Audio file not found: {audio_file_path}")
            return None

        print(f"[EpisodeTranscriber] Transcribing: {audio_file_path}")
        result = self.model.transcribe(audio_file_path)

        padded = str(episode_number).zfill(3)
        
        if output_folder:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder, exist_ok=True)
            output_path = os.path.join(output_folder, f"{padded}.txt")
        else:
            output_path = os.path.join(os.path.dirname(audio_file_path), f"{padded}.txt")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

        print(f"[EpisodeTranscriber] Transcription saved to {output_path}")
        return output_path
