from django.core.paginator import Paginator

from smart_bookmarks.core.interfaces import CreateBookmarkInterface, ScrapePageInterface
from smart_bookmarks.core.models import Bookmark
from smart_bookmarks.core.registry import (
    get_bookmark_service,
    get_scrape_page_service,
    get_search_bookmark_service,
    inject,
)
from smart_bookmarks.core.utils import url_guid
from smart_bookmarks.ui.templatetags.toast_tags import ToastError, ToastInfo


class BookmarkController:

    bookmark_service: CreateBookmarkInterface = inject(get_bookmark_service)
    scrape_service: ScrapePageInterface = inject(get_scrape_page_service)

    def add_bookmark(self, url):
        bookmark_guid = url_guid(url)
        if not Bookmark.objects.guid_exists(bookmark_guid=bookmark_guid):
            return self.bookmark_service.create_bookmark(url)

        return Bookmark.objects.by_guid(bookmark_guid)

    def get_bookmark(self, bookmark_guid):
        return {"bookmark": Bookmark.objects.by_guid(bookmark_guid)}

    def list_bookmarks(self, page_number=1):
        bookmarks = Bookmark.objects.list_all()
        paginator = Paginator(bookmarks, 25)
        return {"bookmarks": paginator.get_page(page_number)}

    def scrape_bookmark(self, bookmark_guid):
        bookmark = Bookmark.objects.by_guid(bookmark_guid)
        if not bookmark:
            return {"toasts": ToastError(message="Bookmark does not exist")}

        self.scrape_service.scrape_page_async(bookmark)
        return {
            "toasts": [ToastInfo(message=f"Scheduled page {bookmark.url} to scrape")]
        }

    def delete_bookmark(self, bookmark_guid):
        Bookmark.objects.delete_by_guid(bookmark_guid)
        return {
            "toasts": [ToastInfo(message=f"Bookmark deleted")],
        }


class SearchController:
    def __init__(self, search_service=get_search_bookmark_service):
        self._search_service = search_service()

    def search_bookmarks(self, query, operator):
        return {
            "bookmark_results": self._search_service.search_bookmarks(query, operator)
        }
