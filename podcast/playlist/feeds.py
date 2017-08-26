"""
Contains the podcast feeds.

"""
import datetime

from django.contrib.syndication.views import Feed
from django.utils.decorators import classonlymethod
from django.utils.feedgenerator import Rss201rev2Feed


class iTunesPodcastsFeedGenerator(Rss201rev2Feed):
    """Feed generator class for the podcast feeds."""

    def rss_attributes(self):
        return {
            u"version": self._version,
            u"xmlns:atom": u"http://www.w3.org/2005/Atom",
            u'xmlns:itunes': u'http://www.itunes.com/dtds/podcast-1.0.dtd'
        }

    def add_root_elements(self, handler):
        super(iTunesPodcastsFeedGenerator, self).add_root_elements(handler)
        handler.addQuickElement(u'itunes:author', self.feed['author_name'])
        handler.addQuickElement(u'itunes:summary', self.feed['description'])
        handler.addQuickElement(u'itunes:explicit',
                                self.feed['iTunes_explicit'])
        handler.startElement(u"itunes:owner", {})
        handler.addQuickElement(u'itunes:name', self.feed['iTunes_name'])
        handler.addQuickElement(u'itunes:email', self.feed['iTunes_email'])
        handler.endElement(u"itunes:owner")
        handler.addQuickElement(u'itunes:image', self.feed['iTunes_image_url'])

    def add_item_elements(self, handler, item):
        super(iTunesPodcastsFeedGenerator, self).add_item_elements(handler,
                                                                   item)
        handler.addQuickElement(u'itunes:summary', item['summary'])
        handler.addQuickElement(u'itunes:explicit', item['explicit'])


class iTunesPlayListFeed(Feed):
    """Feed class for the published playlists."""

    author_name = 'bboogaard'
    iTunes_email = 'padawan@hetnet.nl'
    iTunes_image_url = 'http://example.com/url/of/image'
    iTunes_explicit = 'no'
    feed_type = iTunesPodcastsFeedGenerator

    @classonlymethod
    def as_feed(cls, playlist):
        feed = cls()
        feed.title = playlist.title
        feed.link = playlist.get_absolute_url()
        feed.description = playlist.description
        feed.iTunes_name = playlist.title
        feed.feed_copyright = "Copyright {} by bboogaard".format(
            datetime.date.today().year)
        feed.playlist = playlist
        return feed

    def items(self):
        return self.playlist.files

    def feed_extra_kwargs(self, obj):
        extra = {}
        extra['iTunes_name'] = self.iTunes_name
        extra['iTunes_email'] = self.iTunes_email
        extra['iTunes_image_url'] = self.iTunes_image_url
        extra['iTunes_explicit'] = self.iTunes_explicit
        return extra

    def item_extra_kwargs(self, item):
        return {
            'summary': item.summary,
            'explicit': item.explicit
        }

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.pubdate

    def item_enclosure_url(self, item):
        return item.enclosure_url

    def item_enclosure_length(self, item):
        return item.enclosure_length

    def item_enclosure_mime_type(self, item):
        return item.enclosure_mime_type

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.link
