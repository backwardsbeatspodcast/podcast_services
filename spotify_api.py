import requests
import base64
from datetime import datetime
from secret_management.secret_manager_type import SecretManagerType
from secret_management.secret_manager_factory import secret_manager_factory

class SpotifyAPI:
    def __init__(self, secret_manager_type: SecretManagerType = SecretManagerType.DOTENV):
        self.secret_manager = secret_manager_factory(secret_manager_type)
        self.SPOTIFY_ACCESS_TOKEN = None

    def get_spotify_access_token(self):
        """
        Get the Spotify access token using the client ID and secret stored in the secret manager.
        """
        if self.SPOTIFY_ACCESS_TOKEN:
            return self.SPOTIFY_ACCESS_TOKEN

        auth_url = 'https://accounts.spotify.com/api/token'

        client_id = self.secret_manager.get_secret('spotify_client_id')
        client_secret = self.secret_manager.get_secret('spotify_client_secret')

        if not client_id or not client_secret:
            raise ValueError("Spotify client ID or secret not found in the secret manager")

        auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

        headers = {
            'Authorization': f'Basic {auth_header}'
        }

        payload = {
            'grant_type': 'client_credentials'
        }

        try:
            response = requests.post(auth_url, headers=headers, data=payload)
            response.raise_for_status()

            token_data = response.json()
            self.SPOTIFY_ACCESS_TOKEN = token_data['access_token']
            return self.SPOTIFY_ACCESS_TOKEN

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def get_spotify_artist_id(self, artist_name):
        """
        Get the Spotify ID for a given artist.
        """
        if not self.SPOTIFY_ACCESS_TOKEN:
            self.SPOTIFY_ACCESS_TOKEN = self.get_spotify_access_token()
            if not self.SPOTIFY_ACCESS_TOKEN:
                print("Failed to obtain access token")
                return None

        search_url = 'https://api.spotify.com/v1/search'
        headers = {
            'Authorization': f'Bearer {self.SPOTIFY_ACCESS_TOKEN}'
        }

        params = {
            'q': artist_name,
            'type': 'artist',
            'limit': 1
        }

        try:
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()

            if data['artists']['items']:
                artist_id = data['artists']['items'][0]['id']
                print(f"Artist ID for '{artist_name}': {artist_id}")
                return artist_id
            else:
                print(f"No results found for artist: {artist_name}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def get_album_id(self, artist_name, album_name):
        """
        Get the Spotify ID for a given album by artist_name.
        """
        if not self.SPOTIFY_ACCESS_TOKEN:
            self.SPOTIFY_ACCESS_TOKEN = self.get_spotify_access_token()
            if not self.SPOTIFY_ACCESS_TOKEN:
                print("Failed to obtain access token")
                return None

        search_url = 'https://api.spotify.com/v1/search'
        headers = {
            'Authorization': f'Bearer {self.SPOTIFY_ACCESS_TOKEN}'
        }

        query = f'{album_name}'
        params = {
            'q': query,
            'type': 'album',
            'limit': 1
        }

        try:
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()
            if data['albums']['items']:
                album = data['albums']['items'][0]
                album_id = album['id']
                print(f"Album found: '{album['name']}' by {artist_name}")
                return album_id
            else:
                print(f"No results found for album: '{album_name}' by {artist_name}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def get_album_details(self, album_id):
        """
        Get the details of a Spotify album by its ID.
        """
        if not self.SPOTIFY_ACCESS_TOKEN:
            self.SPOTIFY_ACCESS_TOKEN = self.get_spotify_access_token()
            if not self.SPOTIFY_ACCESS_TOKEN:
                print("Failed to obtain access token")
                return None

        url = f"https://api.spotify.com/v1/albums/{album_id}"
        headers = {
            'Authorization': f'Bearer {self.SPOTIFY_ACCESS_TOKEN}'
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def get_song_id(self, artist_name, song_name):
        """
        Get the Spotify ID for a given song by artist_name.
        """
        if not self.SPOTIFY_ACCESS_TOKEN:
            self.SPOTIFY_ACCESS_TOKEN = self.get_spotify_access_token()
            if not self.SPOTIFY_ACCESS_TOKEN:
                print("Failed to obtain access token")
                return None

        search_url = 'https://api.spotify.com/v1/search'
        headers = {
            'Authorization': f'Bearer {self.SPOTIFY_ACCESS_TOKEN}'
        }

        query = f'{song_name} artist:{artist_name}'
        params = {
            'q': query,
            'type': 'track',
            'limit': 1
        }

        try:
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()
            if data['tracks']['items']:
                song = data['tracks']['items'][0]
                song_id = song['id']
                print(f"Song found: '{song['name']}' by {artist_name}")
                return song_id
            else:
                print(f"No results found for song: '{song_name}' by {artist_name}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def get_song_details(self, song_id):
        """
        Get the details of a Spotify song by its ID.
        """
        if not self.SPOTIFY_ACCESS_TOKEN:
            self.SPOTIFY_ACCESS_TOKEN = self.get_spotify_access_token()
            if not self.SPOTIFY_ACCESS_TOKEN:
                print("Failed to obtain access token")
                return None

        url = f"https://api.spotify.com/v1/tracks/{song_id}"
        headers = {
            'Authorization': f'Bearer {self.SPOTIFY_ACCESS_TOKEN}'
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

