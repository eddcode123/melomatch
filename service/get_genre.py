""" Pyhton script to query spotify
for music genres
"""
import requests
import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

def fetch_spotify_genres():
    # Load Spotify API credentials from environment variables
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    if not client_id or not client_secret:
        raise ValueError("Spotify client credentials not found. Please set them in the .env file.")

    # Fetch access token from Spotify
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    if auth_response.status_code != 200:
        raise Exception(f"Failed to authenticate with Spotify API. Status code: {auth_response.status_code}")

    access_token = auth_response.json()['access_token']

    # Fetch genres from Spotify API
    genres_url = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    genres_response = requests.get(genres_url, headers=headers)

    if genres_response.status_code != 200:
        raise Exception(f"Failed to fetch genres from Spotify API. Status code: {genres_response.status_code}")

    genres_data = genres_response.json()
    genres = genres_data['genres']
    genres.append("Unknown")

    return genres

