"""Module for app utils."""

import dateutil.parser
import babel


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


def get_serialized_show(show):
    """
    Return serialized show.

    :return:
    """
    return {
        'id': show.id,
        'venue_id': show.venue_id,
        'venue_name': show.show_venue.name,
        'venue_image_link': show.show_venue.image_link,
        'artist_id': show.artist_id,
        'artist_name': show.show_artist.name,
        'artist_image_link': show.show_artist.image_link,
        'start_time': str(show.start_time)
    }


def get_serialized_artist(artist):
    """
    Return serialized artist.

    :return:
    """
    upcoming_shows = artist.get_upcoming_shows
    past_shows = artist.get_past_shows
    return {
        "id": artist.id,
        "name": artist.name,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "genres": artist.genres,
        "image_link": artist.image_link,
        "website_link": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }


def get_serialized_venue(venue):
    """
    Return serialized venue.

    :return:
    """
    upcoming_shows = venue.get_upcoming_shows
    past_shows = venue.get_past_shows
    return {
        "id": venue.id,
        "name": venue.name,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "address": venue.address,
        "genres": venue.genres,
        "image_link": venue.image_link,
        "website_link": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }


def serialized_venue_for_list(venue):
    """
    Return serialized venue.

    :return:
    """
    upcoming_shows = venue.get_upcoming_shows
    return {
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": len(upcoming_shows),
    }
