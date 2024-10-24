from dotenv import load_dotenv
import os
from sqlalchemy import (
    create_engine, Column, String, Integer, ForeignKey, Date, Float
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import csv
import sys
from data import add_data
from get_genre import fetch_spotify_genres, get_song_imgurls

# Increase CSV capacity to handle large files
csv.field_size_limit(sys.maxsize)

# Load environment variables from .env file
load_dotenv()

# Retrieve database user and password from environment variables
user = os.getenv('SQLUSER')
password = os.getenv('PASSWORD')

# Create the database engine
database_url = f'mysql+pymysql://{user}:{password}@localhost:3306/Melomatch'
engine = create_engine(database_url)

# Create a base class for the SQLAlchemy models
Base = declarative_base()


class Artist(Base):
    """
    Represents an artist in the database.

    Attributes:
        id (int): Primary key, unique identifier for the artist.
        name (str): The name of the artist.
        songs (relationship): Relationship to the Song model.
    """
    __tablename__ = 'Artist'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(10000))

    # Define relationship to songs
    songs = relationship('Song', back_populates='artist')


class Genre(Base):
    """
    Represents a genre in the database.

    Attributes:
        id (int): Primary key, unique identifier for the genre.
        name (str): The name of the genre.
        songs (relationship): Relationship to the Song model.
    """
    __tablename__ = 'Genre'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(5000))

    # Define relationship to songs
    songs = relationship('Song', back_populates='genre')


class Song(Base):
    """
    Represents a song in the database.

    Attributes:
        id (int): Primary key, unique identifier for the song.
        name (str): The name of the song.
        duration (float): The duration of the song in seconds.
        album (str): The album the song belongs to.
        popularity (int): The popularity of the song.
        image_url (str): song art work
        artist_id (int): Foreign key referencing the artist.
        genre_id (int): Foreign key referencing the genre.
        artist (relationship): Relationship to the Artist model.
        genre (relationship): Relationship to the Genre model.
    """
    __tablename__ = 'Songs'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(5000))
    duration = Column(Float)
    album = Column(String(5000))
    popularity = Column(Integer)
    artist_id = Column(Integer, ForeignKey('Artist.id'))
    genre_id = Column(Integer, ForeignKey('Genre.id'))
    image_url = Column(String(5000))

    # Define relationship to artist and genre
    artist = relationship('Artist', back_populates='songs')
    genre = relationship('Genre', back_populates='songs')


# Create the necessary tables in the database
Base.metadata.create_all(engine)


def get_artist_names():
    """
    Extracts unique artist names from a CSV file and returns them as a list.

    Returns:
        list: A list of unique artist names from the CSV file.
    """
    with open('/home/asavage/Downloads/artists.csv', mode='r') as csv_file:
        artists = list(csv.DictReader(csv_file))
    artist_names = set()  # Use a set to store unique artist names
    for row in artists:
        for key, value in row.items():
            if key == 'artist_mb':
                artist_names.add(value)  # Add to set
    return list(artist_names)  # Convert back to list


# Retrieve artist names from CSV file
artists = get_artist_names()

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Insert artist names into the Artist table
artists_to_insert = [Artist(name=name) for name in artists]
session.bulk_save_objects(artists_to_insert)
session.commit()

print("Artist names added to Artist table")


# Fetch and populate the genre data from Spotify
spotify_genres = fetch_spotify_genres()
genres = [Genre(name=name) for name in spotify_genres]
session.bulk_save_objects(genres)
session.commit()

# Retrieve and process song data
music_data = add_data('/home/asavage/Downloads/songs.csv')

# Add song data to the Songs table
for row in music_data:
    # Find or create the genre for the song
    genre_names = row.get('Genre')
    genre = None
    for value in genre_names:
        genre = session.query(Genre).filter_by(name=value).first()
        if genre:
            break
    if not genre:
        genre = session.query(Genre).filter_by(name='Unknown').first()

    # Get artist data, creating a new artist if necessary
    artist_name = row.get('Artist')
    artist = session.query(Artist).filter_by(name=artist_name).first()
    if not artist:
        artist = Artist(name=artist_name)
        session.add(artist)
        session.commit()

    # Insert the song into the Songs table
    song = Song(
        name=row.get('Name'),
        duration=row.get('Duration'),
        album=row.get('Album'),
        popularity=row.get('Popularity'),
        artist_id=artist.id,
        genre_id=genre.id
    )
    session.add(song)

# Commit the transactions to the database
session.commit()

# add image_url to songs database
songs = session.query(Song).all()

for song in songs:
    img_url = get_song_imgurls(song.name)
    if img_url:
        song.image_url = img_url
    else:
        # set a defualt url to add
        song.image_url = 'https://images.pexels.com/photos/6877350/\
            pexels-photo-\
                6877350.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'
# Commit all updates to the database after processing all songs
session.commit()


# # Print message upon successful completion
# print("Process completed successfully")
