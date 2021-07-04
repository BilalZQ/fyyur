"""Module for app models."""
from datetime import datetime

from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from serializers import show_serializer

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    """Venue Model."""

    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column('genres', db.ARRAY(db.String(120)), nullable=True)
    website_link = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='show_venue', lazy=True, cascade='all, delete-orphan')

    @property
    def get_upcoming_shows(self):
        """
        List of upcoming shows for provided artist.

        :return:
        """
        return show_serializer(Show.query.filter(
            Show.venue_id == self.id, Show.start_time > datetime.now()).all())

    @property
    def get_past_shows(self):
        """
        List of past shows for provided artist.

        :param self:
        :return:
        """
        return show_serializer(Show.query.filter(
            Show.venue_id == self.id, Show.start_time < datetime.now()).all())

    def __repr__(self):
        """
        Return string representation for Venue model.

        :return:
        """
        return f'Venue: {self.name}[{self.id}]'

class Artist(db.Model):
    """Artist model."""

    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column('genres', db.ARRAY(db.String(120)), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120), nullable=False)
    shows = db.relationship('Show', backref='show_artist', lazy=True, cascade='all, delete-orphan')

    @property
    def get_upcoming_shows(self):
        """
        List of upcoming shows for provided artist.

        :return:
        """
        return show_serializer(Show.query.filter(
            Show.artist_id == self.id, Show.start_time > datetime.now()).all())

    @property
    def get_past_shows(self):
        """
        List of past shows for provided artist.

        :param self:
        :return:
        """
        return show_serializer(Show.query.filter(
            Show.artist_id == self.id, Show.start_time < datetime.now()).all())

    def __repr__(self):
        """
        Return string representation for Artist model.

        :return:
        """
        return f'Artist Id: {self.name}[{self.id}]'


class Show(db.Model):
    """Show Model."""

    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    start_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """
        Return string representation for show model.

        :return:
        """
        return f'<Show: {self.id}, Artist: {self.artist_id}, Venue: {self.venue_id}>'
