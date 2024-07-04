# create our database models

from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Date,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Artists(Base):
    # create artist table 
    __tablename__ = 'Artist'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(150), unique=True)

    # define relationship to songs
    songs = relationship('Song', back_populates='artist')

class Genre(Base):
    # create table
    __tablename__ = 'Genre'

    # create columns 
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(150))
    # define relationship to songs
    songs = relationship('Song', back_populates='genre')
# create song database
class Song(Base):
    # create dong table
    __tablename__ = 'Songs'

    # create table columns
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(200))
    genre = Column(ForeignKey(Genre.id))
    duration = Column(Float)
    album = Column(String(200))
    release = Column(Date)
    artistid = Column(ForeignKey(Artists.id))

    # define relationship to artist and genre
    artist = relationship('Artist', back_populates='songs')
    genre = relationship('Genre', back_populates='songs')


# created the database

# populate database