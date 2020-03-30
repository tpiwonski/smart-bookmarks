import abc
from dataclasses import dataclass
from typing import List, Optional

from smart_bookmarks.core.models import Bookmark, Page


class CreateBookmarkInterface(abc.ABC):
    @abc.abstractmethod
    def create_bookmark(self, url: str) -> Bookmark:
        """TODO"""


@dataclass
class PageData:
    title: str
    description: str
    text: str
    source: str


class CreatePageInterface(abc.ABC):
    @abc.abstractmethod
    def create_page(self, bookmark: Bookmark, page_data: PageData) -> Page:
        """TODO"""


class ScrapePageInterface(abc.ABC):
    @abc.abstractmethod
    def scrape_page_async(self, bookmark: Bookmark):
        """TODO"""


class IndexBookmarkInterface(abc.ABC):
    @abc.abstractmethod
    def index_bookmark_async(self, bookmark: Bookmark):
        """TODO"""

    @abc.abstractmethod
    def index_bookmark(self, bookmark: Bookmark):
        """TODO"""

    @abc.abstractmethod
    def index_bookmark_by_id(self, bookmark_id):
        """TODO"""


@dataclass
class BookmarkHighlights:
    url: List[str]
    title: List[str]
    description: List[str]
    text: List[str]


@dataclass
class BookmarkResult:
    bookmark: Bookmark
    score: float
    highlights: BookmarkHighlights


@dataclass
class SearchResults:
    total_hits: int
    max_score: float
    results: List[BookmarkResult]

    def count(self):
        return self.total_hits


class SearchBookmarkInterface(abc.ABC):
    @abc.abstractmethod
    def search_bookmarks(
        self, query: str, operator: str, offset: Optional[int], limit: Optional[int]
    ) -> SearchResults:
        """TODO"""


class ImportBookmarkInterface(abc.ABC):
    @abc.abstractmethod
    def import_file(self, file_path: str):
        """TODO"""
