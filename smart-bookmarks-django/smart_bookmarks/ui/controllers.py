from smart_bookmarks.core.registry import get_search_service, get_bookmark_service


class BookmarkController:

    def __init__(self, bookmark_service=get_bookmark_service):
        self._bookmark_service = bookmark_service()

    def create_bookmark(self, url):
        return self._bookmark_service.create_bookmark(url)


class SearchController:

    def __init__(self, search_service=get_search_service):
        self._search_service = search_service()

    def search_bookmarks(self, query, operator):
        return self._search_service.search_bookmarks(query, operator)
