from django.db import transaction

from smart_bookmarks.core.models import Bookmark, Page
from smart_bookmarks.core.registry import get_scrape_service, get_index_service
from smart_bookmarks.core.utils import url_guid


class BookmarkService:

    def __init__(self, scrape_service=get_scrape_service):
        self._scrape_service = scrape_service()

    @transaction.atomic
    def create_bookmark(self, url):
        guid = url_guid(url)
        bookmark = Bookmark.objects.create(guid=guid, url=url)
        self._scrape_service.scrape_page_async(bookmark)
        return bookmark


class PageService:

    def __init__(self, index_service=get_index_service):
        self._index_service = index_service()

    @transaction.atomic
    def create_page(self, bookmark, page_text):
        page = Page.objects.create(bookmark=bookmark, text=page_text)
        self._index_service.index_page_async(page)
        return page
