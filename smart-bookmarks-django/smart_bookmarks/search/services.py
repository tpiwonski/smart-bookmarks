import logging

from django.conf import settings
from django.utils.timezone import now

from smart_bookmarks.core.interfaces import IndexBookmarkInterface, SearchBookmarkInterface, FoundBookmark, \
    BookmarkHighlights
from smart_bookmarks.core.models import Bookmark, Page
from smart_bookmarks.core.registry import inject
from smart_bookmarks.search.elasticsearch import ElasticsearchService, BookmarkData
from smart_bookmarks.search.models import IndexBookmark


LOGGER = logging.getLogger(__name__)


OPERATOR_AND = 'and'
OPERATOR_OR = 'or'
OPERATORS = [
    (OPERATOR_AND, OPERATOR_AND),
    (OPERATOR_OR, OPERATOR_OR)]


class IndexBookmarkService(IndexBookmarkInterface):

    search_bookmark_service = inject(lambda: ElasticsearchService(settings.ELASTICSEARCH_HOST))

    def index_bookmark_async(self, bookmark):
        index_bookmark = IndexBookmark.objects.create(bookmark=bookmark)
        LOGGER.info("Index bookmark created: index_bookmark_id=%s, bookmark_id=%s", index_bookmark.id, bookmark.id)

    def index_bookmark(self, bookmark: Bookmark):
        bookmark_data = BookmarkData(
            id=bookmark.id,
            url=bookmark.url,
            title=bookmark.page.title if bookmark.page else None,
            description=bookmark.page.description if bookmark.page else None,
            text=bookmark.page.text if bookmark.page else None)

        self.search_bookmark_service.index_bookmark(bookmark_data)
        bookmark.indexed = now()
        bookmark.save(update_fields=['updated', 'indexed'])
        LOGGER.info("Bookmark indexed: bookmark_id=%s", bookmark.id)

    def index_bookmark_by_id(self, bookmark_id):
        bookmark = Bookmark.objects.by_id(bookmark_id)
        if bookmark is None:
            LOGGER.info("Bookmark does not exist: bookmark_id=%s", bookmark_id)
            return

        self.index_bookmark(bookmark)


class SearchBookmarkService(SearchBookmarkInterface):

    search_bookmark_service = inject(lambda: ElasticsearchService(settings.ELASTICSEARCH_HOST))

    def search_bookmarks(self, query, operator):
        search_results = self.search_bookmark_service.search_bookmark(query, operator)
        found_bookmarks = [
            FoundBookmark(
                bookmark=Bookmark.objects.get(id=found_bookmark.meta.id),
                score=found_bookmark.meta.score,
                highlights=BookmarkHighlights(
                    url=self.get_highlight(found_bookmark.meta.highlight, 'url'),
                    title=self.get_highlight(found_bookmark.meta.highlight, 'title'),
                    description=self.get_highlight(found_bookmark.meta.highlight, 'description'),
                    text=self.get_highlight(found_bookmark.meta.highlight, 'text')))
            for found_bookmark in search_results]

        return found_bookmarks

    @staticmethod
    def get_highlight(highlight, field):
        try:
            return highlight[field]
        except KeyError:
            return []
