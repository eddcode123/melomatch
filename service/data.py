import requests
from dotenv import load_dotenv
import os
import csv
import sys

# Load environment variables
load_dotenv()

# Increase CSV capacity
csv.field_size_limit(sys.maxsize)


def get_artist_names(path):
    """Extract artist names from a CSV file."""

    with open(path, mode='r') as csv_file:
        artists = list(csv.DictReader(csv_file))
    artist_names = set()  # Use a set to store unique artist names
    for row in artists:
        artist_name = row.get('artist_mb')
        if artist_name:
            artist_names.add(artist_name)
    return list(artist_names)


def get_songs(path):
    """Retrieve songs from a CSV file."""
    with open(path, 'r') as f:
        songs = list(csv.DictReader(f))
    return songs


def fetch_additional_data(api_key, artist, song):
    """Fetch additional data for a song from the Last.fm API."""
    url = f'https://ws.audioscrobbler.com/2.0/?method=track.getInfo&api' \
        f'key={api_key}&artist={artist}&track={song}&format=json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        track_info = data.get('track')
        if track_info:
            duration = track_info.get('duration', 'Unknown')
            genres = [tag['name'] for tag in track_info.get('toptags', {}).get('tag', [])]
            return duration, genres if genres else 'Unknown'
    return None, 'Unknown'


def add_data(path):
    """Add additional data to songs from a CSV file."""
    api_key = os.getenv('APIKEY')
    if not api_key:
        raise ValueError("API key not found. Please set it in the .env file.")

    songs = get_songs(path)

    for row in songs:
        artist = row.get('Artist')
        song = row.get('Name')
        if not artist or not song:
            continue

        duration, genres = fetch_additional_data(api_key, artist, song)
        row['Duration'] = duration
        row['Genre'] = genres

    return songs
