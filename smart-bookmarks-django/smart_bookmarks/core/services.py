from django.conf import settings
from django.db import transaction

from smart_bookmarks.core.signals import bookmark_created, page_created
from smart_bookmarks.core.models import Bookmark, Page
from smart_bookmarks.core.utils import url_guid, service_instance


class BookmarkService:

    # def __init__(self):
        # self._scraper_service = service_instance(settings.SCRAPER_SERVICE)

    @transaction.atomic
    def create_bookmark(self, url):
        guid = url_guid(url)
        bookmark = Bookmark.objects.create(guid=guid, url=url)
        # self._scraper_service.scrape_page_async(bookmark)
        bookmark_created.send(sender=self, bookmark=bookmark)
        return bookmark


class PageService:

    @transaction.atomic
    def create_page(self, bookmark, page_text):
        page = Page.objects.create(bookmark=bookmark, text=page_text)
        page_created.send(sender=self, page=page)
        return page
