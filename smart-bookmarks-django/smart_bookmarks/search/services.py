import logging
from dataclasses import dataclass
from typing import List

from django.conf import settings
from django.utils.timezone import now

from smart_bookmarks.core.interfaces import (
    BookmarkHighlights,
    BookmarkResult,
    IndexBookmarkInterface,
    SearchBookmarkInterface,
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


class SearchQuery:
    def __init__(self, query, operator):
        self.query = query
        self.operator = operator


class SearchQuerySet:
    def __init__(self, service, query: SearchQuery, page_number: int, per_page: int):
        self.service = service
        self.query = query
        self.page_number = page_number
        self.per_page = per_page
        self.total_hits = None
        self.max_score = None
        self.cached_results = {}

    def count(self):
        if self.total_hits is not None:
            return self.total_hits

        self.load((self.page_number - 1) * self.per_page, self.per_page)
        return self.total_hits

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.load(item.start, item.stop - item.start)

        for (offset, length), results in self.cached_results.items():
            if offset <= item <= offset + length - 1:
                return results[item - offset]

        results = self.load(item, self.per_page)
        return results[0]

    def load(self, offset, length):
        if length == 0:
            return []

        cached_results = self.cached_results.get((offset, length))
        if cached_results:
            return cached_results

        results = self.service.search_q(query=self.query, offset=offset, length=length,)

        self.total_hits = results.total_hits
        self.max_score = results.max_score
        self.cached_results[(offset, len(results.results))] = results.results

        return results.results


@dataclass
class SearchResults:
    total_hits: int
    max_score: float
    results: List[BookmarkResult]


class SearchBookmarkService(SearchBookmarkInterface):

    search_bookmark_service = inject(
        lambda: ElasticsearchService(settings.ELASTICSEARCH_HOST)
    )

    def search(self, query: str, operator: str, page_number: int, per_page: int):
        return SearchQuerySet(self, SearchQuery(query, operator), page_number, per_page)

    def search_q(self, query, offset: int, length: int):
        search_results = self.search_bookmark_service.search_bookmark(
            query.query, query.operator, offset=offset, limit=length
        )

        total_hits = search_results["hits"]["total"]["value"]
        max_score = search_results["hits"]["max_score"]

        bookmark_results = {}
        for bookmark_result in search_results["hits"]["hits"]:
            score = bookmark_result["_score"]
            bookmark_id = bookmark_result["_id"]
            highlight = bookmark_result["highlight"]
            highlight_url = highlight.get("url")
            highlight_title = highlight.get("title")
            highlight_description = highlight.get("description")
            highlight_text = highlight.get("text")

            bookmark_results[int(bookmark_id)] = dict(
                score=score,
                highlights=BookmarkHighlights(
                    url=highlight_url,
                    title=highlight_title,
                    description=highlight_description,
                    text=highlight_text,
                ),
            )

        bookmarks = BookmarkResult.objects.by_ids(bookmark_ids=bookmark_results.keys())

        for bookmark in bookmarks:
            bookmark.score = bookmark_results[bookmark.id]["score"]
            bookmark.highlights = bookmark_results[bookmark.id]["highlights"]

        return SearchResults(
            total_hits=total_hits, max_score=max_score, results=bookmarks
        )
