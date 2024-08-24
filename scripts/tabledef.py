# -*- coding: utf-8 -*-

import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Heroku
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

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

    searchid = Column(Integer, primary_key=True)
    longitude = Column(Float)
    latitude = Column(Float)

    # Relationship to Bycatch
    bycatches = relationship("Bycatch", back_populates="search")

    def __repr__(self):
        return '<Search %r>' % self.searchid


class Bycatch(Base):
    __tablename__ = "bycatch"

    id = Column(Integer, primary_key=True)
    fish = Column(String(50))
    index = Column(Integer)
    searchid = Column(Integer, ForeignKey('search.searchid'))

    # Relationship to Search
    search = relationship("Search", back_populates="bycatches")

    def __repr__(self):
        return '<Bycatch %r>' % self.fish


# Connect to the database
engine = db_connect()

# Create all tables in the database
Base.metadata.create_all(engine)
