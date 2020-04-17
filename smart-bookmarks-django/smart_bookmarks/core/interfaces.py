import abc
from dataclasses import dataclass
from typing import List, Optional, Sequence

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
class BookmarkSearchHighlights:
    url: List[str] = None
    title: List[str] = None
    description: List[str] = None
    text: List[str] = None


@dataclass
class BookmarkSearchResult:
    score: float = None
    highlights: BookmarkSearchHighlights = None
    bookmark: Bookmark = None


@dataclass
class BookmarkSearchResults:
    total_results: int = None
    max_score: float = None
    results: List[BookmarkSearchResult] = None


class SearchBookmarkInterface(abc.ABC):
    @abc.abstractmethod
    def search(
        self, query: str, operator: str, page_number: int, per_page: int
    ) -> BookmarkSearchResults:
        """TODO"""


class ImportBookmarkInterface(abc.ABC):
    @abc.abstractmethod
    def import_file(self, file_path: str):
        """TODO"""
