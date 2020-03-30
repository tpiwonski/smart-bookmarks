import logging

from django.conf import settings
from django.utils.timezone import now

from smart_bookmarks.core.interfaces import (
    BookmarkHighlights,
    BookmarkResult,
    IndexBookmarkInterface,
    SearchBookmarkInterface,
    SearchResults,
)
from smart_bookmarks.core.models import Bookmark
from smart_bookmarks.core.registry import inject
from smart_bookmarks.search.elasticsearch import BookmarkData, ElasticsearchService
from smart_bookmarks.search.models import IndexBookmarkTask

LOGGER = logging.getLogger(__name__)

OPERATOR_AND = "and"
OPERATOR_OR = "or"
OPERATORS = [(OPERATOR_AND, OPERATOR_AND), (OPERATOR_OR, OPERATOR_OR)]


class IndexBookmarkService(IndexBookmarkInterface):

    search_bookmark_service = inject(
        lambda: ElasticsearchService(settings.ELASTICSEARCH_HOST)
    )

    def index_bookmark_async(self, bookmark):
        task = IndexBookmarkTask.objects.task_by_bookmark_id(bookmark.id)
        if not task:
            task = IndexBookmarkTask.objects.create(bookmark=bookmark)
        else:
            task.save(update_fields=["updated"])

        LOGGER.info(
            "Index bookmark created: index_bookmark_id=%s, bookmark_id=%s",
            task.id,
            bookmark.id,
        )

    def index_bookmark(self, bookmark: Bookmark):
        bookmark_data = BookmarkData(
            id=bookmark.id,
            url=bookmark.url,
            title=bookmark.page.title if bookmark.page else None,
            description=bookmark.page.description if bookmark.page else None,
            text=bookmark.page.text if bookmark.page else None,
        )

        self.search_bookmark_service.index_bookmark(bookmark_data)
        bookmark.indexed = now()
        bookmark.save(update_fields=["updated", "indexed"])
        LOGGER.info("Bookmark indexed: bookmark_id=%s", bookmark.id)

    def index_bookmark_by_id(self, bookmark_id):
        bookmark = Bookmark.objects.by_id(bookmark_id)
        if bookmark is None:
            LOGGER.info("Bookmark does not exist: bookmark_id=%s", bookmark_id)
            return

        self.index_bookmark(bookmark)


class SearchBookmarkService(SearchBookmarkInterface):

    search_bookmark_service = inject(
        lambda: ElasticsearchService(settings.ELASTICSEARCH_HOST)
    )

    def search_bookmarks(self, query, operator, offset=None, limit=None):
        search_results = self.search_bookmark_service.search_bookmark(
            query, operator, offset=offset, limit=limit
        )

        total_hits = search_results["hits"]["total"]["value"]
        max_score = search_results["hits"]["max_score"]

        bookmark_results = []
        for bookmark_result in search_results["hits"]["hits"]:

            score = bookmark_result["_score"]
            bookmark_id = bookmark_result["_id"]
            highlight = bookmark_result["highlight"]
            highlight_url = highlight.get("url")
            highlight_title = highlight.get("title")
            highlight_description = highlight.get("description")
            highlight_text = highlight.get("text")

            bookmark = Bookmark.objects.by_id(bookmark_id)
            if not bookmark:
                continue

            bookmark_results.append(
                BookmarkResult(
                    bookmark=bookmark,
                    score=score,
                    highlights=BookmarkHighlights(
                        url=highlight_url,
                        title=highlight_title,
                        description=highlight_description,
                        text=highlight_text,
                    ),
                )
            )

        return SearchResults(
            total_hits=total_hits, max_score=max_score, results=bookmark_results
        )
