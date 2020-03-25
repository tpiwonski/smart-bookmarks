from smart_bookmarks.core.interfaces import ScrapePageInterface, CreateBookmarkInterface
from smart_bookmarks.core.models import Bookmark
from smart_bookmarks.core.registry import get_search_bookmark_service, get_bookmark_service, inject, \
    get_scrape_page_service
from smart_bookmarks.core.utils import url_guid


class BookmarkController:

    bookmark_service: CreateBookmarkInterface = inject(get_bookmark_service)
    scrape_service: ScrapePageInterface = inject(get_scrape_page_service)

    def add_bookmark(self, url):
        bookmark_guid = url_guid(url)
        if not Bookmark.objects.guid_exists(bookmark_guid=bookmark_guid):
            return self.bookmark_service.create_bookmark(url)

        return Bookmark.objects.by_guid(bookmark_guid)

    def scrape_bookmark(self, bookmark_guid):
        bookmark = Bookmark.objects.by_guid(bookmark_guid)
        if not bookmark:
            return None

        self.scrape_service.scrape_page_async(bookmark)
        return bookmark

    def delete_bookmark(self, bookmark_guid):
        Bookmark.objects.delete_by_guid(bookmark_guid)


class SearchController:

    def __init__(self, search_service=get_search_bookmark_service):
        self._search_service = search_service()

    def search_bookmarks(self, query, operator):
        return self._search_service.search_bookmarks(query, operator)
