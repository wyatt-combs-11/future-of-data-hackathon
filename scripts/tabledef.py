# -*- coding: utf-8 -*-

import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


def get_database_url():
    # Heroku being a pain
    url = os.getenv('DATABASE_URL')
    if url and url.startswith('postgres://'):
        return url.replace('postgres://', 'postgresql://', 1)
    return url


# Heroku
SQLALCHEMY_DATABASE_URI = get_database_url()

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(SQLALCHEMY_DATABASE_URI)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    password = Column(String(512))
    email = Column(String(50))

    def __repr__(self):
        return '<User %r>' % self.username


class Search(Base):
    __tablename__ = "search"

    search_id = Column(Integer, primary_key=True)
    longitude = Column(Float)
    latitude = Column(Float)

    # Relationship to Bycatch
    bycatches = relationship("Bycatch", back_populates="search")

    def __repr__(self):
        return '<Search %r>' % self.search_id


class Bycatch(Base):
    __tablename__ = "bycatch"

    id = Column(Integer, primary_key=True)
    fish = Column(String(50))
    index = Column(Integer)
    search_id = Column(Integer, ForeignKey('search.search_id'))

    # Relationship to Search
    search = relationship("Search", back_populates="bycatches")

    def __repr__(self):
        return '<Bycatch %r>' % self.fish


# Connect to the database
engine = db_connect()

# Create all tables in the database
Base.metadata.create_all(engine)
