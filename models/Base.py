from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Date, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import csv
import sys
from data import add_data
from get_genre import fetch_spotify_genres

# increase csv capacity
csv.field_size_limit(sys.maxsize)

# Load environment variables
load_dotenv()

# Set database user and password
user = os.getenv('SQLUSER')
password = os.getenv('PASSWORD')

# Create the database engine
database_url = f'mysql+pymysql://{user}:{password}@localhost:3306/Melomatch'
engine = create_engine(database_url)

# Create a base class for our models
Base = declarative_base()

# Define the Artists model
class Artist(Base):
    __tablename__ = 'Artist'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(10000))

    # Define relationship to songs
    songs = relationship('Song', back_populates='artist')

# Define the Genre model
class Genre(Base):
    __tablename__ = 'Genre'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(5000))

    # Define relationship to songs
    songs = relationship('Song', back_populates='genre')

# Define the Song model
class Song(Base):
    __tablename__ = 'Songs'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(5000))
    duration = Column(Float)
    album = Column(String(5000))
    popularity = Column(Integer)
    artist_id = Column(Integer, ForeignKey('Artist.id'))
    genre_id = Column(Integer, ForeignKey('Genre.id'))

    # Define relationship to artist and genre
    artist = relationship('Artist', back_populates='songs')
    genre = relationship('Genre', back_populates='songs')

# Create tables in the database
Base.metadata.create_all(engine)

# how i inserted artist data in the database
"""
# Extract artist data
def get_artist_names():
    with open('/home/asavage/Downloads/artists.csv', mode='r') as csv_file:
        artists = list(csv.DictReader(csv_file))
    artist_names = set()  # Use a set to store unique artist names
    for row in artists:
        for key, value in row.items():
            if key == 'artist_mb':
                artist_names.add(value)  # Add to set
    return list(artist_names)  # Convert back to list

artists = get_artist_names()

# Populate database
Session  = sessionmaker(bind=engine)
session = Session()
# Insert artist names in the artist table
artists_to_insert = [Artist(name=name) for name in artists]
session.bulk_save_objects(artists_to_insert)
session.commit()

#artists = get_artist_names('/home/asavage/Downloads/artists.csv')

 """
# Populate database
Session  = sessionmaker(bind=engine)
session = Session()
# the add data function does two things which are
# gets data artist from a cvs file
# since data from the cvs file has missing data like "duration, genre"
# the add_data fuction also uses lastfm api to get missing data of every song.
# it also adds the missing feilds in the music data
# add geners to Genre table
""" spotify_genres = fetch_spotify_genres()
generes = [Genre(name=name) for name in spotify_genres]
session.bulk_save_objects(generes)
session.commit() """

music_data = add_data('/home/asavage/Downloads/songs.csv') 
 # adding data to songs table 
for row in music_data:
    # Add genre to genre table
    genre_names = row.get('Genre')
    genre = None
    for value in genre_names:
        genre = session.query(Genre).filter_by(name=value).first()
        if genre:
            break
    if not genre:
        genre = session.query(Genre).filter_by(name='Unknown').first()

    # get artist data
    artist_name = row.get('Artist')
    # query the database to see if artist exist
    artist = session.query(Artist).filter_by(name=artist_name).first()
    # add artist if they don't exist in songs table
    if not artist:
        artist = Artist(name=artist_name)
        session.add(artist)
        session.commit()
    # add data to the Songs table
    song = Song(
        name = row.get('Name'),
        duration = row.get('Duration'),
        album = row.get('Album'),
        popularity = row.get('Popularity'),
        artist_id = artist.id,
        genre_id = genre.id
    )
    session.add(song)
# commit the transactions
session.commit()
# prinyt message if everything works well
print("Process complete Successfuly")
