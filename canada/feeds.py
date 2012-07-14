from django.contrib.syndication.views import Feed

from .apps.artists.models import Artist
from .apps.exhibitions.models import Exhibition
from .apps.press.models import Press
from .apps.updates.models import Update


class AllEntriesFeed(Feed):
    title = "CANADA feed"
    link = "/"
    description = "Updates on changes and additions to canadanewyork.com."

    def items(self):
        return Update.objects.order_by('-post_date')[:5]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description
