import requests
from shared_services import BaseAPI
from secret_management.secret_manager_type import SecretManagerType


class SpotifyAPI(BaseAPI):
    """
    SpotifyAPI class for interacting with the Spotify Web API.
    This class handles authentication and provides methods to retrieve artist, album, and song information.
    It uses the client_credentials grant type for authentication.
    """

    BASE_URL = 'https://api.spotify.com/v1'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'

    def __init__(self, secret_manager_type=SecretManagerType.DOTENV):
        self.client_id_key = 'SPOTIFY_CLIENT_ID'
        self.client_secret_key = 'SPOTIFY_CLIENT_SECRET'
        super().__init__(
            secret_manager_type,
            token_url=self.TOKEN_URL,
            client_id_key=self.client_id_key,
            client_secret_key=self.client_secret_key,
        )
        self._access_token = None
    


    def get_access_token(self):
        """
        Overrides or extends BaseAPI's token retrieval for Spotify's Basic auth token request.
        """
        if self._access_token:
            return self._access_token

        client_id = self.secret_manager.get_secret(self.client_id_key)
        client_secret = self.secret_manager.get_secret(self.client_secret_key)

        if not client_id or not client_secret:
            print("[SpotifyAPI] Missing client ID or secret.")
            return None

        auth_header = requests.auth._basic_auth_str(client_id, client_secret)

        headers = {'Authorization': auth_header}
        payload = {'grant_type': 'client_credentials'}

        try:
            response = requests.post(self.token_url, headers=headers, data=payload)
            response.raise_for_status()
            token_data = response.json()
            self._access_token = token_data.get('access_token')
            return self._access_token
        except requests.RequestException as e:
            print(f"[SpotifyAPI] Failed to get access token: {e}")
            return None

    def _make_get_request(self, endpoint: str, params: dict = None):
        """
        Makes a GET request to the Spotify API.
            :param endpoint: The API endpoint to call.
            :param params: Optional parameters for the request.
            :return: The JSON response from the API.
        """
        access_token = self.get_access_token()
        if not access_token:
            print("[SpotifyAPI] No access token available.")
            return None

        headers = {'Authorization': f'Bearer {access_token}'}
        url = f'{self.BASE_URL}/{endpoint}'

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[SpotifyAPI] Error calling '{endpoint}': {e}")
            return None

    # Spotify mostly uses GET requests for API calls below, so no need for POST method here.

    def get_artist_id(self, artist_name: str):
        """
        Retrieves the Spotify ID of an artist by their name.
            :param artist_name: The name of the artist.
            :return: The Spotify ID of the artist.
        """
        params = {'q': artist_name, 'type': 'artist', 'limit': 1}
        data = self._make_get_request('search', params)
        if data and data.get('artists', {}).get('items'):
            artist_id = data['artists']['items'][0]['id']
            print(f"Artist ID for '{artist_name}': {artist_id}")
            return artist_id
        print(f"No results found for artist: {artist_name}")
        return None

    def get_artist_details(self, artist_id: str):
        """
        Retrieves details of an artist using their Spotify ID.
            :param artist_id: The Spotify ID of the artist.
            :return: The details of the artist.
        """
        return self._make_get_request(f'artists/{artist_id}')

    def get_album_id(self, artist_name: str, album_name: str):
        """
        Retrieves the Spotify ID of an album by its name and artist.
            :param artist_name: The name of the artist.
            :param album_name: The name of the album.
            :return: The Spotify ID of the album.
        """
        params = {'q': album_name, 'type': 'album', 'limit': 1}
        data = self._make_get_request('search', params)
        if data and data.get('albums', {}).get('items'):
            album = data['albums']['items'][0]
            print(f"Album found: '{album['name']}'")
            return album['id']
        print(f"No results found for album: '{album_name}'")
        return None

    def get_album_details(self, album_id: str):
        """
        Retrieves details of an album using its Spotify ID. 
            :param album_id: The Spotify ID of the album.
            :return: The details of the album.
        """
        return self._make_get_request(f'albums/{album_id}')

    def get_song_id(self, artist_name: str, song_name: str):
        """
        Retrieves the Spotify ID of a song by its name and artist.
            :param artist_name: The name of the artist.
            :param song_name: The name of the song.
            :return: The Spotify ID of the song.
        """
        query = f'{song_name} artist:{artist_name}'
        params = {'q': query, 'type': 'track', 'limit': 1}
        data = self._make_get_request('search', params)
        if data and data.get('tracks', {}).get('items'):
            song = data['tracks']['items'][0]
            print(f"Song found: '{song['name']}' by {artist_name}")
            return song['id']
        print(f"No results found for song: '{song_name}' by {artist_name}")
        return None

    def get_song_details(self, song_id: str):
        """
        Retrieves details of a song using its Spotify ID.
            :param song_id: The Spotify ID of the song.
            :return: The details of the song.
        """
        return self._make_get_request(f'tracks/{song_id}')

