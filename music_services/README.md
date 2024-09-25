# Music Services 
Provides a unified interface for interacting with various music APIs. 
This subpackage currently supports the Spotify API and is designed to allow easy retrieval 
of information about artists, albums, and songs.

## Interface Overview
Currently the package only supports Spotify. As such all the examples will use that service.

### SpotifyAPI
The SpotifyAPI class provides methods for interacting with the Spotify API. Below are the available methods and their descriptions:
The data returned by the methods is in JSON format and defined by the [Spotify REST API](https://developer.spotify.com/documentation/web-api/reference/search).

* `get_artist_id(self, artist_name)`: Searches for an artist by name and returns the corresponding Spotify ID.
* `get_album_id(self, artist_name, album_name)`: Searches for an album by the artist's name and album title, returning the album ID.
* `get_album_details(self, album_id)`: Retrieves detailed information about a specific album using its Spotify ID.
* `get_song_id(self, artist_name, song_name)`: Searches for a song by artist name and song title, returning the song ID.
* `get_song_details(self, song_id)`: Retrieves detailed information about a specific song using its Spotify ID.


## Usage examples
Below are some examples of how to use the SpotifyAPI class to retrieve information about artists, albums, and songs.

### Initialize the SpotifyAPI class

```python
from secret_management.secret_manager_type import SecretManagerType
from secret_management.secret_manager_factory import secret_manager_factory
from music_services import SpotifyAPI

# Create a SecretManager instance
secret_manager = secret_manager_factory(SecretManagerType.DOTENV)
spotify_api = SpotifyAPI(secret_manager)
```

### Get artist information
```python
artist_id = spotify_api.get_artist_id("The Beatles")
artist_details = spotify_api.get_artist_details(artist_id)
```
### Get album information
```python
album_id = spotify_api.get_album_id("The Beatles", "Abbey Road")
album_details = spotify_api.get_album_details(album_id)
``` 
### Get song information
```python
song_id = spotify_api.get_song_id("The Beatles", "Come Together")
song_details = spotify_api.get_song_details(song_id)
```
