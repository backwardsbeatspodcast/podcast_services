import unittest
from music_services.spotify_api import SpotifyAPI  # Adjust the path as needed

class TestSpotifyAPIIntegration(unittest.TestCase):
    def test_get_artist_id(self):
        api = SpotifyAPI()
        artist_name = "Radiohead"
        artist_id = api.get_artist_id(artist_name)

        self.assertIsNotNone(artist_id, "Artist ID should not be None")
        self.assertIsInstance(artist_id, str, "Artist ID should be a string")
        # print(f"Artist ID for {artist_name}: {artist_id}")

    def test_get_artist_details(self):
        api = SpotifyAPI()
        artist_id = api.get_artist_id("Radiohead")
        artist_details = api.get_artist_details(artist_id)

        self.assertIsNotNone(artist_details, "Artist details should not be None")
        self.assertIsInstance(artist_details, dict, "Artist details should be a dictionary")
        self.assertEqual(artist_details["name"].lower(), "radiohead", "Artist name mismatch")
        # print(f"Artist Details: {artist_details}")

    def test_get_album_id(self):
        api = SpotifyAPI()
        album_id = api.get_album_id("Radiohead", "OK Computer")

        self.assertIsNotNone(album_id, "Album ID should not be None")
        self.assertIsInstance(album_id, str, "Album ID should be a string")
        # print(f"Album ID: {album_id}")

    def test_get_album_details(self):
        api = SpotifyAPI()
        album_id = api.get_album_id("Radiohead", "OK Computer")
        album_details = api.get_album_details(album_id)

        self.assertIsNotNone(album_details, "Album details should not be None")
        self.assertIsInstance(album_details, dict, "Album details should be a dictionary")
        self.assertEqual(album_details["name"].lower(), "ok computer", "Album name mismatch")

