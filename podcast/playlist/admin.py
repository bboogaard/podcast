"""
ModelAdmins for the playlist app.

"""
from django.contrib import admin

from podcast.playlist import models


admin.site.register(models.PlayListFile)
