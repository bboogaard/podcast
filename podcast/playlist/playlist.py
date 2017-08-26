"""
Contains the Playlist definitions.

"""
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.functional import lazy

from podcast.playlist import models


class PlayListFile(object):
    """Wrapper for playlist file objects."""

    def __init__(self, playlist_file, categories):
        self.title = playlist_file.title
        self.link = playlist_file.get_file_url()
        self.pubdate = playlist_file.publication_datetime
        self.author_name = 'bboogaard'
        self.categories = categories
        self.description = playlist_file.description

        self.enclosure_url = playlist_file.get_file_url()
        self.enclosure_length = playlist_file.file.size
        self.enclosure_mime_type = 'audio/mpeg'

        self.summary = playlist_file.description
        self.explicit = 'no'

    def get_absolute_url(self):
        return self.link


class PlayList(object):
    """Playlist definition."""

    def __init__(self, title, slug, description, categories):
        self.title = title
        self.slug = slug
        self.description = description
        self.categories = categories

    @property
    def files(self):
        return [
            PlayListFile(playlist_file, self.categories)
            for playlist_file in models.PlayListFile.objects.filter(
                playlist=self.slug
            )
        ]

    def get_absolute_url(self):
        return lazy(lambda: settings.PLAYLIST_URL + reverse(
            'playlists:{}.rss'.format(self.slug)), str)


playlists = [
    PlayList(
        playlist['TITLE'],
        playlist['SLUG'],
        playlist['DESCRIPTION'],
        playlist['CATEGORIES']
    )
    for playlist in settings.PLAYLISTS
]
