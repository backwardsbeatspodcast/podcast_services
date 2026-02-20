# tests/integration/test_ai_services_real.py
import unittest
import os
import tempfile
import shutil
from pathlib import Path
from ai_services.transcription import EpisodeTranscriber

class TestEpisodeTranscriberReal(unittest.TestCase):
    def setUp(self):
        # Initialize with the smallest model for speed
        self.transcriber = EpisodeTranscriber(model_size="tiny")
        
        # Setup paths
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.test_audio_path = self.project_root / "tests" / "data" / "test.mp3"
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_real_transcription(self):
        """Actually run the transcription on the test mp3 file."""
        self.assertTrue(self.test_audio_path.exists(), f"Test audio file not found at {self.test_audio_path}")
        
        print(f"\n[Test] Starting real transcription of {self.test_audio_path} using 'tiny' model...")
        
        # This might take a few moments depending on the system
        result_path = self.transcriber.transcribe_episode(
            str(self.test_audio_path), 
            episode_number=1, 
            output_folder=self.temp_dir
        )
        
        expected_output_path = os.path.join(self.temp_dir, "001.txt")
        self.assertEqual(result_path, expected_output_path)
        self.assertTrue(os.path.exists(expected_output_path))
        
        with open(expected_output_path, "r", encoding="utf-8") as f:
            transcription_text = f.read().strip()
            print(f"[Test] Transcription result: '{transcription_text}'")
            self.assertGreater(len(transcription_text), 0, "Transcription result should not be empty")

if __name__ == '__main__':
    unittest.main()
