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


class BookmarkResult(Bookmark):
    score: float
    highlights: BookmarkHighlights

    class Meta:
        proxy = True


class SearchBookmarkInterface(abc.ABC):
    @abc.abstractmethod
    def search(
        self, query: str, operator: str, page_number: int, per_page: int
    ) -> List[BookmarkResult]:
        """TODO"""


class ImportBookmarkInterface(abc.ABC):
    @abc.abstractmethod
    def import_file(self, file_path: str):
        """TODO"""
