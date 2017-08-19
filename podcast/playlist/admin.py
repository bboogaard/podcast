"""
ModelAdmins for the playlist app.

"""
import os
from django.contrib import admin

from podcast.playlist import models


class PlayListFileInline(admin.StackedInline):

    model = models.PlayListFile


class PlayListAdmin(admin.ModelAdmin):

    inlines = [PlayListFileInline]

admin.site.register(models.PlayList, PlayListAdmin)
