from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Date, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import csv

# Load environment variables
load_dotenv()

# Set database user and password
user = os.getenv('SQLUSER')
password = os.getenv('PASSWORD')

# Create the database engine
database_url = f'mysql+pymysql://{user}:{password}@localhost:3306/Melomatch'
print(database_url)
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
    name = Column(String(150))

    # Define relationship to songs
    songs = relationship('Song', back_populates='genre')

# Define the Song model
class Song(Base):
    __tablename__ = 'Songs'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(200))
    genre_id = Column(Integer, ForeignKey('Genre.id'))
    duration = Column(Float)
    album = Column(String(200))
    release = Column(Date)
    artist_id = Column(Integer, ForeignKey('Artist.id'))

    # Define relationship to artist and genre
    artist = relationship('Artist', back_populates='songs')
    genre = relationship('Genre', back_populates='songs')

# Create tables in the database
Base.metadata.create_all(engine)

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