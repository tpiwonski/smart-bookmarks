import logging

from django.conf import settings

from smart_bookmarks.core.models import Bookmark, Page
from smart_bookmarks.search.elasticsearch import ElasticsearchService
from smart_bookmarks.search.models import IndexPage


LOGGER = logging.getLogger(__name__)


class IndexService:

    def __init__(self):
        self._search_service = ElasticsearchService(settings.ELASTICSEARCH_HOST)

    def index_page_async(self, page):
        index_page = IndexPage.objects.create(page=page)
        LOGGER.info("Index page created: index_page_id=%s, page_id=%s", index_page.id, page.id)

    def index_page(self, page):
        self._search_service.index_page(page)
        LOGGER.info("Page indexed: page_id=%s", page.id)

    def index_page_by_id(self, page_id):
        try:
            page = Page.objects.by_id(page_id)
        except Page.DoesNotExist:
            LOGGER.info("Page does not exist: page_id=%s", page_id)
            return

        self._search_service.index_page(page)


class SearchService:

    def __init__(self):
        self._search_service = ElasticsearchService(settings.ELASTICSEARCH_HOST)

    def search_bookmarks(self, term):
        pages = self._search_service.search_page(term)
        page_ids = [page.meta.id for page in pages]
        return Bookmark.objects.by_page_ids(page_ids)
