import requests
import base64
from datetime import datetime
from google.colab import userdata

"""
This module provides functions to interact with the Spotify API to retrieve information about artists and albums.
As it uses the Spotify Web API, you will need to provide your Spotify client ID and secret in the Colab secrets.
"""

# Global variable to store the access token
SPOTIFY_ACCESS_TOKEN = None

def get_spotify_access_token():
    """
    Get the Spotify access token using the client ID and secret stored in Colab secrets.
    """
    global SPOTIFY_ACCESS_TOKEN
    if SPOTIFY_ACCESS_TOKEN:
        return SPOTIFY_ACCESS_TOKEN

    auth_url = 'https://accounts.spotify.com/api/token'

    client_id = userdata.get('spotify_client_id')
    client_secret = userdata.get('spotify_client_secret')

    if not client_id or not client_secret:
        raise ValueError("Spotify client ID or secret not found in Colab secrets")

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
        SPOTIFY_ACCESS_TOKEN = token_data['access_token']
        return SPOTIFY_ACCESS_TOKEN

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_spotify_artist_id(artist_name):
    """
    Get the Spotify ID for a given artist artist_name
    """
    global SPOTIFY_ACCESS_TOKEN
    if not SPOTIFY_ACCESS_TOKEN:
        SPOTIFY_ACCESS_TOKEN = get_spotify_access_token()
        if not SPOTIFY_ACCESS_TOKEN:
            print("Failed to obtain access token")
            return None

    search_url = 'https://api.spotify.com/v1/search'

    headers = {
        'Authorization': f'Bearer {SPOTIFY_ACCESS_TOKEN}'
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


def get_spotify_album_id(artist_name, album_name):
    """
    Get the Spotify ID for a given album by artist_name
    """

    global SPOTIFY_ACCESS_TOKEN
    if not SPOTIFY_ACCESS_TOKEN:
        SPOTIFY_ACCESS_TOKEN = get_spotify_access_token()
        if not SPOTIFY_ACCESS_TOKEN:
            print("Failed to obtain access token")
            return None

    search_url = 'https://api.spotify.com/v1/search'

    headers = {
        'Authorization': f'Bearer {SPOTIFY_ACCESS_TOKEN}'
    }

    # Construct the query to search for the album by the specific artist
    # query = f'album:{album_name} artist:{artist_name}'
    query = f'{album_name}'
    print('Query: ', query)

    params = {
        'q': query,
        'type': 'album',
        'limit': 1
    }

    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        print(data)
        if data['albums']['items']:
            album = data['albums']['items'][0]
            album_id = album['id']
            album_name = album['name']
            release_date = album['release_date']
            total_tracks = album['total_tracks']

            print(f"Album found: '{album_name}' by {artist_name}")
            print(f"Album ID: {album_id}")
            print(f"Release Date: {release_date}")
            print(f"Total Tracks: {total_tracks}")

            return album_id
        else:
            print(f"No results found for album: '{album_name}' by {artist_name}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None



def get_spotify_album_details(album_id):
    """
    Get the details of a Spotify album by its ID
    """

    global SPOTIFY_ACCESS_TOKEN
    if not SPOTIFY_ACCESS_TOKEN:
        SPOTIFY_ACCESS_TOKEN = get_spotify_access_token()
        if not SPOTIFY_ACCESS_TOKEN:
            print("Failed to obtain access token")
            return None

    url = f"https://api.spotify.com/v1/albums/{album_id}"

    params = {
        'market': 'US',
        'locale': 'en-US,en;q=0.9'
    }

    headers = {
        'Authorization': f'Bearer {SPOTIFY_ACCESS_TOKEN}'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        album_data = response.json()
        return album_data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def format_date(date_string, precision):
    """
    Format the date string based on the precision (day|month|year[default]).
    """

    if precision == 'day':
        return datetime.strptime(date_string, '%Y-%m-%d').strftime('%B %d, %Y')
    elif precision == 'month':
        return datetime.strptime(date_string, '%Y-%m').strftime('%B %Y')
    else:  # year
        return date_string  # Already in YYYY format

def get_medium_image(images):
    """
    Get the URL of the medium-sized image from the list of images.
    """

    if len(images) >= 2:
        return images[1]['url']  # Medium size is typically the second image
    elif images:
        return images[0]['url']  # If only one image, return that
    return None

def generate_album_markdown(album_details):
    """
    Generate a Markdown template for the album details.
    """

    if not album_details:
        return "Failed to retrieve album details"

    markdown = "---\n"
    markdown += f"artist: {album_details['artists'][0]['name']}\n"
    markdown += f"rank: '__RANK__'\n"
    markdown += f"album: {album_details['name']}\n"
    markdown += "status: Production\n"
    markdown += "tags:\n"
    markdown += "---\n\n"

    markdown += f"# {album_details['name']}\n\n"
    markdown += f"**Artist:** {album_details['artists'][0]['name']}\n"
    markdown += f"**Rank:** __RANK__\n"

    release_date = format_date(album_details['release_date'], album_details['release_date_precision'])
    markdown += f"**Release Date:** {release_date}\n"

    markdown += f"**Total Tracks:** {album_details['total_tracks']}\n"
    markdown += f"**Album URL:** [{album_details['name']}]({album_details['external_urls']['spotify']})\n\n"

    medium_image_url = get_medium_image(album_details.get('images', []))
    if medium_image_url:
        markdown += f"![Album Cover]({medium_image_url})\n\n"

    markdown += "__WIKI_SUMMARY__\n"
    # markdown += "[more info...](__WIKI_URL__)\n\n"

    markdown += "## Tracks\n\n"
    counter = 1
    for track in album_details['tracks']['items']:
        markdown += f"{counter}. [{track['name']}]({track['external_urls']['spotify']})\n"
        counter = counter + 1

    return markdown
