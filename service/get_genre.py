""" Pyhton script to query spotify
for music genres
"""
import requests
import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

def fetch_spotify_genres():
    """
    Fetches a list of available genres from the Spotify API.

    Returns:
        list: A list of genres available on Spotify, including an 'Unknown' genre.

    Raises:
        ValueError: If Spotify API credentials are not found in environment variables.
        Exception: If authentication with Spotify API fails or if genres cannot be retrieved.
    """
    # Load Spotify API credentials from environment variables
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    # Raise error if credentials are missing
    if not client_id or not client_secret:
        raise ValueError(
            "Spotify client credentials not found. "
            "Please set them in the .env file."
        )

    # Fetch access token from Spotify
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    # Check if authentication is successful
    if auth_response.status_code != 200:
        raise Exception(
            f"Failed to authenticate with Spotify API. "
            f"Status code: {auth_response.status_code}"
        )

    # Extract access token from response
    access_token = auth_response.json()['access_token']

    # Fetch genres from Spotify API
    genres_url = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
    
    # Set up authorization header
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Send GET request to Spotify API to retrieve available genres
    genres_response = requests.get(genres_url, headers=headers)

    # Check if request is successful
    if genres_response.status_code != 200:
        raise Exception(
            f"Failed to fetch genres from Spotify API. "
            f"Status code: {genres_response.status_code}"
        )

    # Parse genres data
    genres_data = genres_response.json()
    genres = genres_data['genres']  # Extract genres list

    # Append an 'Unknown' genre to the list
    genres.append("Unknown")

    return genres


def get_track_id(track_name):
    """
    Fetches the Spotify track ID for a given track name.

    Args:
        track_name (str): The name of the track to search for.

    Returns:
        str: The Spotify track ID if found.
        int: The status code if an error occurs during the request.

    Raises:
        ValueError: If Spotify API credentials are not found in environment variables.
        Exception: If authentication with Spotify API fails.
    """
    # Load Spotify API credentials from environment variables
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    # Raise error if credentials are missing
    if not client_id or not client_secret:
        raise ValueError(
            "Spotify client credentials not found. "
            "Please set them in the .env file."
        )

    # Fetch access token from Spotify
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    # Check if authentication is successful
    if auth_response.status_code != 200:
        raise Exception(
            f"Failed to authenticate with Spotify API. "
            f"Status code: {auth_response.status_code}"
        )

    # Extract access token from response
    access_token = auth_response.json()['access_token']

    # Set up Spotify API search URL
    get_id_url = 'https://api.spotify.com/v1/search'
    
    # Set up authorization header
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Set up search parameters to find the track
    params = {
        'q': track_name,
        'type': 'track',
        'limit': 1
    }

    # Send GET request to Spotify API to search for the track
    response = requests.get(get_id_url, headers=headers, params=params)

    # Check if request is successful
    if response and response.status_code == 200:
        data = response.json()
        items = data['tracks']['items']
        if items:  # Ensure there's at least one track found
            track_id = items[0]['id']  # Extract the track ID
            album_id = items[0]['album']['id']  # Extract the album ID
            return track_id, album_id

    return None, None # Return None if no track was found


def get_song_imgurls(name_of_song):
    """
    Retrieves the image URL of a song's album artwork from the Spotify API.

    Args:
        name_of_song (str): The name of the song for which the image URL is requested.

    Returns:
        str: The URL of the album artwork image if successful.

    Raises:
        ValueError: If Spotify API credentials are not found in environment variables.
        Exception: If authentication with Spotify API fails or if the image URL cannot be retrieved.
    """
    # Load Spotify API credentials from environment variables
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    # Raise error if credentials are missing
    if not client_id or not client_secret:
        raise ValueError(
            "Spotify client credentials not found. "
            "Please set them in the .env file."
        )

    # Fetch access token from Spotify
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    # Check if authentication is successful
    if auth_response.status_code != 200:
        raise Exception(
            f"Failed to authenticate with Spotify API. "
            f"Status code: {auth_response.status_code}"
        )

    # Extract access token from response
    access_token = auth_response.json()['access_token']

    # Set up authorization header
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Get track info, including the album ID
    track_id, album_id = get_track_id(name_of_song)

    if not album_id:
        raise Exception("Album ID not found for the given track.")

    # Use Spotify API to get song artwork
    get_song_artwork_url = f'https://api.spotify.com/v1/albums/{album_id}'

    # Request song artwork
    response = requests.get(get_song_artwork_url, headers=headers)

    # Check if request was successful
    if response and response.status_code == 200:
        # Parse the data to get the image URL
        data = response.json()
        image_url = data["images"][0]["url"]  # Use [0] to get the first image in the list
        return image_url
    
    # Return the status code if the request was not successful
    return response.status_code

# test code 
print(get_song_imgurls('beautiful things'))
