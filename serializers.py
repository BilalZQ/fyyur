"""Module for serializers."""
from utils import (
    get_serialized_show, get_serialized_artist, get_serialized_venue
)


def show_serializer(shows, multiple=True):
    """
    Show serializer.

    :param shows:
    :param multiple:
    :return:
    """
    return [get_serialized_show(show) for show in shows] if multiple \
        else get_serialized_show(shows)


def artist_serializer(artists, multiple=True):
    """
    Artist serializer.

    :param artists:
    :param multiple:
    :return:
    """
    return [get_serialized_artist(artist) for artist in artists] if multiple \
        else get_serialized_artist(artists)


def venue_serializer(venues, multiple=True):
    """
    Venue serializer.

    :param venues:
    :param multiple:
    :return:
    """
    return [get_serialized_venue(venue) for venue in venues] if multiple \
        else get_serialized_venue(venues)
