from flask import Flask, jsonify
import pymysql
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set global variables for database connection
SQLUSER = os.getenv('SQLUSER')
HOST = os.getenv('HOST')
PASSWD = os.getenv('PASSWORD')
DB = os.getenv('DATABASE')


def mysql_connector(query):
    """
    Establishes a connection to the MySQL database and executes
    the provided SQL query.

    Args:
        query (str): The SQL query to be executed.

    Returns:
        tuple: The result set fetched from the database.
    """
    # Create a connection to the MySQL database
    conn = pymysql.connect(
        host=HOST,
        user=SQLUSER,
        password=PASSWD,
        db=DB
    )

    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    # Execute the SQL query
    cur.execute(query)

    # Fetch all results from the executed query
    data = cur.fetchall()

    # Close the cursor and connection
    cur.close()

    return data


# Create the Flask app
app = Flask(__name__)


def get_artist_and_genre_names(artist_id, genre_id):
    """
    Fetches the artist and genre names based on their IDs from the database.

    Args:
        artist_id (int): The ID of the artist.
        genre_id (int): The ID of the genre.

    Returns:
        tuple: A tuple containing the artist's name and the genre's name.
    """
    # Query to fetch artist name by artist ID
    artist_query = f"SELECT name FROM Artist WHERE id = {artist_id}"
    artist = mysql_connector(artist_query)
    artist_name = artist[0][0] if artist else "Unknown Artist"

    # Query to fetch genre name by genre ID
    genre_query = f"SELECT name FROM Genre WHERE id = {genre_id}"
    genre = mysql_connector(genre_query)
    genre_name = genre[0][0] if genre else "Unknown Genre"

    return artist_name, genre_name


@app.route('/all-music')
def get_random_10songs():
    """
    API endpoint to retrieve 10 random songs with their
    artist and genre names.

    Returns:
        Response: A JSON response containing a list of 10 songs,
            each with its name, duration, artist name, and genre name.
    """
    # SQL query to fetch 10 songs
    query = 'SELECT name, duration, artist_id, \
        genre_id FROM Songs ORDER BY name LIMIT 10;'
    data = list(mysql_connector(query))

    # Prepare a list to store song data
    songs_data = []

    # Iterate over the retrieved songs and get artist and genre names
    for song in data:
        name, duration, artist_id, genre_id = song
        artist_name, song_genre = get_artist_and_genre_names(artist_id, genre_id)

        # Append song data to the list
        songs_data.append({
            'name': name,
            'duration': duration,
            'artist': artist_name,
            'genre': song_genre
        })

    # Return the data as a JSON response
    return jsonify(songs_data)


# Run the Flask app
if __name__ == '__main__':
    app.run()
