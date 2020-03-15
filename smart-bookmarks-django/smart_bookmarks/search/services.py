import logging

from django.conf import settings

from smart_bookmarks.core.interfaces import IndexBookmarkInterface, SearchBookmarkInterface
from smart_bookmarks.core.models import Bookmark, Page
from smart_bookmarks.core.registry import inject
from smart_bookmarks.search.elasticsearch import ElasticsearchService
from smart_bookmarks.search.models import IndexPage


LOGGER = logging.getLogger(__name__)


OPERATOR_AND = 'and'
OPERATOR_OR = 'or'
OPERATORS = [
    (OPERATOR_AND, OPERATOR_AND),
    (OPERATOR_OR, OPERATOR_OR)]


class IndexBookmarkService(IndexBookmarkInterface):

    search_bookmark_service = inject(lambda: ElasticsearchService(settings.ELASTICSEARCH_HOST))

    def index_page_async(self, page):
        index_page = IndexPage.objects.create(page=page)
        LOGGER.info("Index page created: index_page_id=%s, page_id=%s", index_page.id, page.id)

    def index_page(self, page):
        self.search_bookmark_service.index_page(page)
        LOGGER.info("Page indexed: page_id=%s", page.id)

    def index_page_by_id(self, page_id):
        page = Page.objects.by_id(page_id)
        if page is None:
            LOGGER.info("Page does not exist: page_id=%s", page_id)
            return

        self.index_page(page)


class SearchBookmarkService(SearchBookmarkInterface):

    search_bookmark_service = inject(lambda: ElasticsearchService(settings.ELASTICSEARCH_HOST))

    def search_bookmarks(self, query, operator):
        pages = self.search_bookmark_service.search_page(query, operator)
        page_ids = [page.meta.id for page in pages]
        return Bookmark.objects.by_page_ids(page_ids)
