"""
Development settings.

"""
from .base import *

# Django settings #

DEBUG = True

ALLOWED_HOSTS = '*'

MEDIA_ROOT = '/home/bboogaard/data/podcast'
MEDIA_URL = 'http://www.dev.autokopen.nl:5022/media/'

# Project settings #
PLAYLIST_URL = 'http://www.dev.autokopen.nl:5022'
