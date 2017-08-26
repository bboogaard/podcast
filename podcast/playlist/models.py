"""
Models for the playlist app.

"""
import os

import magic
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def playlist_file_upload_to(instance, filename):
    """Upload handler for the PlayListFile.file field."""
    return instance.filename


def validate_file(value):
    """Validator for the PlayListFile.file field."""
    file = magic.Magic(mime=True)
    type = file.from_buffer(value.read())
    if type != 'audio/mpeg':
        raise ValidationError('Ongeldig bestandstype')


available_playlists = [
    (playlist['SLUG'], playlist['TITLE'])
    for playlist in settings.PLAYLISTS
]


class PlayListFile(models.Model):
    """Contains the playlist files."""

    #: Description of the audio file
    description = models.TextField('Samenvatting', blank=True)

    #: The audio file
    file = models.FileField(
        upload_to=playlist_file_upload_to, blank=True,
        validators=[validate_file],
        help_text=("Toegestaan: .mp3"),
        verbose_name='Bestand'
    )

    #: The playlist the file belongs to
    playlist = models.CharField(
        'Playlist', max_length=20, choices=available_playlists)

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
        return os.path.join('playlist', self.playlist, self.slug) + '.mp3'

    def get_file_url(self):
        return settings.MEDIA_URL + self.filename
