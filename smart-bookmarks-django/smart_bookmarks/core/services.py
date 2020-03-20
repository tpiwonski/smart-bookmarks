from django.db import transaction

from smart_bookmarks.core.interfaces import CreateBookmarkInterface, CreatePageInterface
from smart_bookmarks.core.models import Bookmark, Page
from smart_bookmarks.core.registry import get_scrape_page_service, get_index_bookmark_service, inject
from smart_bookmarks.core.utils import url_guid


class BookmarkService(CreateBookmarkInterface):

    scrape_page_service = inject(get_scrape_page_service)
    index_page_service = inject(get_index_bookmark_service)

    @transaction.atomic
    def create_bookmark(self, url):
        guid = url_guid(url)
        bookmark = Bookmark.objects.create(guid=guid, url=url)
        self.index_page_service.index_bookmark_async(bookmark)
        self.scrape_page_service.scrape_page_async(bookmark)
        return bookmark


class PageService(CreatePageInterface):

    index_page_service = inject(get_index_bookmark_service)

    @transaction.atomic
    def create_page(self, bookmark, page_data):
        page = Page.objects.by_bookmark_id(bookmark.id)
        if page:
            page.title = page_data.title
            page.description = page_data.description
            page.text = page_data.text
            page.source = page_data.source
            page.save(update_fields=['title', 'description', 'text', 'source'])
        else:
            page = Page.objects.create(
                bookmark=bookmark, title=page_data.title, description=page_data.description, text=page_data.text,
                source=page_data.source)

        self.index_page_service.index_bookmark_async(bookmark)
        return page
