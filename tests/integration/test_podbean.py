import unittest
from podbean_services.podbean_api import PodbeanAPI

class TestPodbeanAPIIntegration(unittest.TestCase):
    def test_get_podcast(self):
        api = PodbeanAPI()
        podcast_info = api.get_podcast()
        
        self.assertIsNotNone(podcast_info, "Podcast information should not be None")
        self.assertIsInstance(podcast_info, dict)
        self.assertIn('podcast', podcast_info, "Podcast information should contain 'podcast' key")

    def test_get_episodes(self):
        api = PodbeanAPI()
        limit = 1
        episodes_info = api.get_episodes(offset=0, limit=limit)
        
        self.assertIsNotNone(episodes_info, "Episodes information should not be None")
        self.assertIsInstance(episodes_info, dict, "Episodes information should be a dictionary")
        self.assertIn("episodes", episodes_info, "Response should contain 'episodes' key")
        self.assertIsInstance(episodes_info["episodes"], list, "'episodes' should be a list")
        self.assertLessEqual(len(episodes_info["episodes"]), limit, f"Should return no more than {limit} episodes")
        #print(f"Episodes Information: {episodes_info}")

    def test_get_episode(self):
        api = PodbeanAPI()
        episode_id = "99U4B18B6780"
        episode_info = api.get_episode(episode_id)
        self.assertIsNotNone(episode_info, "Episode information should not be None")
        #print(f"Episode Information: {episode_info}")

if __name__ == '__main__':
    unittest.main()

