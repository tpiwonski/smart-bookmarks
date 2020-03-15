import abc
from dataclasses import dataclass

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
    def index_page_async(self, page: Page):
        """TODO"""

    @abc.abstractmethod
    def index_page(self, page: Page):
        """TODO"""


class SearchBookmarkInterface(abc.ABC):

    @abc.abstractmethod
    def search_bookmarks(self, query: str, operator: str):
        """TODO"""


class ImportBookmarkInterface(abc.ABC):

    @abc.abstractmethod
    def import_file(self, file_path: str):
        """TODO"""
