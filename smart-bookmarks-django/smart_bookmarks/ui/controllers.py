from smart_bookmarks.core.models import Bookmark
from smart_bookmarks.core.registry import get_search_bookmark_service, get_bookmark_service
from smart_bookmarks.core.utils import url_guid


class BookmarkController:

    def __init__(self, bookmark_service=get_bookmark_service):
        self._bookmark_service = bookmark_service()

    def add_bookmark(self, url):
        bookmark_guid = url_guid(url)
        if not Bookmark.objects.guid_exists(bookmark_guid=bookmark_guid):
            return self._bookmark_service.create_bookmark(url)

        return Bookmark.objects.by_guid(bookmark_guid)


class SearchController:

    def __init__(self, search_service=get_search_bookmark_service):
        self._search_service = search_service()

    def search_bookmarks(self, query, operator):
        return self._search_service.search_bookmarks(query, operator)
