from django.core.paginator import Page, Paginator

from smart_bookmarks.core.interfaces import (
    CreateBookmarkInterface,
    ScrapePageInterface,
    SearchBookmarkInterface,
)
from smart_bookmarks.core.models import Bookmark
from smart_bookmarks.core.registry import (
    get_bookmark_service,
    get_scrape_page_service,
    get_search_bookmark_service,
    inject,
)
from smart_bookmarks.core.utils import url_guid
from smart_bookmarks.search.services import OPERATOR_AND
from smart_bookmarks.ui.toast import ErrorMessage, InfoMessage

PAGE_SIZE = 3


class BookmarkController:

    bookmark_service: CreateBookmarkInterface = inject(get_bookmark_service)
    scrape_service: ScrapePageInterface = inject(get_scrape_page_service)
    search_service: SearchBookmarkInterface = inject(get_search_bookmark_service)

    def add_bookmark(self, url):
        bookmark_guid = url_guid(url)
        if not Bookmark.objects.guid_exists(bookmark_guid=bookmark_guid):
            return self.bookmark_service.create_bookmark(url)

        return Bookmark.objects.by_guid(bookmark_guid)

    def get_bookmark(self, bookmark_guid):
        return {"bookmark": Bookmark.objects.by_guid(bookmark_guid)}

    def list_bookmarks(self, query=None, operator=OPERATOR_AND, page_number=1):
        if query:
            offset = None if page_number == 1 else (page_number - 1) * PAGE_SIZE
            bookmarks = self.search_service.search_bookmarks(
                query, operator, offset, PAGE_SIZE
            )
            bookmarks = Page(
                object_list=bookmarks.results,
                number=page_number,
                paginator=Paginator(object_list=bookmarks, per_page=PAGE_SIZE),
            )
        else:
            bookmarks = Bookmark.objects.list_all()
            paginator = Paginator(bookmarks, PAGE_SIZE)
            bookmarks = paginator.get_page(page_number)

        return {"bookmarks": bookmarks}

    def scrape_bookmark(self, bookmark_guid):
        bookmark = Bookmark.objects.by_guid(bookmark_guid)
        if not bookmark:
            return {"messages": [ErrorMessage(message="Bookmark does not exist")]}

        self.scrape_service.scrape_page_async(bookmark)
        return {
            "messages": [
                InfoMessage(message=f"Scheduled page {bookmark.url} to scrape")
            ]
        }

    def delete_bookmark(self, bookmark_guid):
        Bookmark.objects.delete_by_guid(bookmark_guid)
        return {
            "messages": [InfoMessage(message=f"Bookmark deleted")],
        }
