"""
Url patterns for the playlist app.

"""
from django.conf.urls import url

from podcast.playlist.feeds import iTunesPlayListFeed
from podcast.playlist.playlist import playlists


urlpatterns = []
for playlist in playlists:
    urlpatterns.append(url(r'{}.rss$'.format(playlist.slug), iTunesPlayListFeed.as_feed(playlist), name='{}.rss'.format(playlist.slug)))
