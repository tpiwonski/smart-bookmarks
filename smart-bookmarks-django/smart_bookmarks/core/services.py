from django.conf import settings
from django.db import transaction

from smart_bookmarks.core.models import Bookmark, Page
from smart_bookmarks.core.utils import url_guid, service_instance


class BookmarkService:

    def __init__(self):
        self._scraper_service = service_instance(settings.SCRAPER_SERVICE)

    @transaction.atomic
    def create_bookmark(self, url):
        guid = url_guid(url)
        bookmark = Bookmark.objects.create(guid=guid, url=url)
        self._scraper_service.scrape_page_async(bookmark)
        return bookmark


class PageService:

    def __init__(self):
        self._index_service = service_instance(settings.INDEX_SERVICE)

    @transaction.atomic
    def create_page(self, bookmark, page_text):
        page = Page.objects.create(bookmark=bookmark, text=page_text)
        self._index_service.index_page_async(page)
        return page
