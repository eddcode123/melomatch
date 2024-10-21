from flask import Flask, Request, jsonify
import pymysql
import os
from dotenv import load_dotenv

# load env variables
load_dotenv()

# create Global variables
SQLUSER = os.getenv('SQLUSER')
HOST = os.getenv('HOST')
PASSWD = os.getenv('PASSWORD')
DB = os.getenv('DATABASE')

# create a pymysql connector
def mysql_connector(query):
    conn = pymysql.connect(
        host= HOST,
        user= SQLUSER,
        password= PASSWD,
        db= DB
    )
    # create a cursor
    cur = conn.cursor()

    # execute a sql query
    cur.execute(query)
    # store data retrived from database
    data = cur.fetchall()
    # close the connection 
    cur.close()

    return data
# create api app
app = Flask(__name__)

# Helper function to get artist and genre names by their IDs
def get_artist_and_genre_names(artist_id, genre_id):
    # Query to get artist name
    artist_query = f"SELECT name FROM Artist WHERE id = {artist_id}"
    artist = mysql_connector(artist_query)
    artist_name = artist[0][0] if artist else "Unknown Artist"

    # Query to get genre name
    genre_query = f"SELECT name FROM Genre WHERE id = {genre_id}"
    genre = mysql_connector(genre_query)
    genre_name = genre[0][0] if genre else "Unknown Genre"

    return artist_name, genre_name

# create api endpoints for music data
@app.route('/all-music')
def get_random_10songs():
    query = 'select name, duration, artist_id, genre_id from Songs order by name limit 10;'
    data = list(mysql_connector(query))


    # create a dictionary with the data
    songs_data = []

    # Iterate over the data and fetch artist and genre names
    for song in data:
        name, duration, artist_id, genre_id = song
        artist_name , song_genre = get_artist_and_genre_names(artist_id, genre_id)

        #append song data to list
        songs_data.append({
            'name': name,
            'duration': duration,
            'artist': artist_name,
            'genre': song_genre
        })
    
    return jsonify(songs_data)


# starting server
if __name__ == '__main__':
    app.run(debug=True)