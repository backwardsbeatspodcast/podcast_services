# tests/unit/test_ai_services.py
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import tempfile
import shutil
from pathlib import Path

# Mock whisper and pydub for the test
mock_whisper = MagicMock()
mock_pydub = MagicMock()
sys.modules['whisper'] = mock_whisper
sys.modules['pydub'] = mock_pydub

from ai_services.transcription import EpisodeTranscriber

class TestEpisodeTranscriber(unittest.TestCase):
    @patch('ai_services.transcription.whisper')
    def setUp(self, mock_transcription_whisper):
        self.mock_model = MagicMock()
        mock_transcription_whisper.load_model.return_value = self.mock_model
        self.transcriber = EpisodeTranscriber(model_size="tiny")
        
        # Setup paths
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.test_audio_path = self.project_root / "tests" / "data" / "test.mp3"
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_init(self):
        self.assertEqual(self.transcriber.model_size, "tiny")

    def test_transcribe_episode_with_real_input_file(self):
        # Ensure the test file exists
        self.assertTrue(self.test_audio_path.exists(), f"Test audio file not found at {self.test_audio_path}")
        
        self.mock_model.transcribe.return_value = {"text": "Hello from test mp3"}
        
        # Test transcription with specific output folder
        result_path = self.transcriber.transcribe_episode(
            str(self.test_audio_path), 
            episode_number=99, 
            output_folder=self.temp_dir
        )
        
        expected_output_path = os.path.join(self.temp_dir, "099.txt")
        self.assertEqual(result_path, expected_output_path)
        self.assertTrue(os.path.exists(expected_output_path))
        
        with open(expected_output_path, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "Hello from test mp3")

    def test_transcribe_episode_default_output(self):
        # For default output, it uses the directory of the audio file.
        # To avoid writing to tests/data, we'll copy the test file to our temp dir.
        temp_audio_path = os.path.join(self.temp_dir, "test.mp3")
        shutil.copy(self.test_audio_path, temp_audio_path)
        
        self.mock_model.transcribe.return_value = {"text": "Default output test"}
        
        result_path = self.transcriber.transcribe_episode(temp_audio_path, 7)
        
        expected_output_path = os.path.join(self.temp_dir, "007.txt")
        self.assertEqual(result_path, expected_output_path)
        self.assertTrue(os.path.exists(expected_output_path))
        
        with open(expected_output_path, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "Default output test")

if __name__ == '__main__':
    unittest.main()
