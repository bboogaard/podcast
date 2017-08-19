"""
Models for the playlist app.

"""
import os

import magic
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class PlayList(models.Model):
    """Contains the playlists to be published."""

    #: Description of the playlist
    description = models.TextField('Omschrijving', blank=True)

    #: Playlist published yes/no?
    published = models.BooleanField('Gepubliceerd', default=False)

    #: The slug of the playlist
    slug = models.SlugField('Slug', max_length=20, unique=True)

    #: The title of the playlist
    title = models.CharField('Naam', max_length=100, blank=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'

    def __unicode__(self):
        return self.title


def playlist_file_upload_to(instance, filename):
    """Upload handler for the PlayListFile.file field."""
    return instance.filename


def validate_file(value):
    """Validator for the PlayListFile.file field."""
    file = magic.Magic(mime=True)
    type = file.from_buffer(value.read())
    if type != 'audio/mpeg':
        raise ValidationError('Ongeldig bestandstype')


class PlayListFile(models.Model):
    """Contains the playlist files."""

    #: The audio file
    file = models.FileField(
        upload_to=playlist_file_upload_to, blank=True,
        validators=[validate_file],
        help_text=("Toegestaan: .mp3"),
        verbose_name='Bestand'
    )

    #: The playlist the file belongs to
    playlist = models.ForeignKey(
        PlayList, related_name='files', on_delete=models.deletion.CASCADE,
        verbose_name='Playlist')

    #: Publication time of the file
    publication_datetime = models.DateTimeField('Gepubliceerd op')

    #: The slug of the audio file
    slug = models.SlugField('Slug', max_length=20, unique=True)

    #: Title of the audio file
    title = models.CharField('Naam', max_length=100, blank=True)

    class Meta:
        ordering = ['playlist', 'publication_datetime']
        verbose_name = 'Audiobestand'
        verbose_name_plural = 'Audiobestanden'

    def __unicode__(self):
        return self.title

    @property
    def filename(self):
        return os.path.join('playlist', self.playlist.slug, self.slug) + '.mp3'

    def get_file_url(self):
        return settings.MEDIA_URL + self.filename
