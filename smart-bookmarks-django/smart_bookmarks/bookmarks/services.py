from django.conf import settings
from django.db import transaction

from smart_bookmarks.bookmarks.models import Bookmark
from smart_bookmarks.bookmarks.utils import url_guid, service_instance


class BookmarkService:

    def __init__(self):
        self._scraper_service = service_instance(settings.SCRAPER_SERVICE)

    @transaction.atomic
    def add_bookmark(self, url):
        guid = url_guid(url)
        bookmark = Bookmark.objects.create(guid=guid, url=url)
        self._scraper_service.enqueue_scrape_page_task(bookmark)
        return bookmark
