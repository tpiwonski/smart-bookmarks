import abc

from smart_bookmarks.core.models import Bookmark, Page


class ScrapeServiceInterface(abc.ABC):

    @abc.abstractmethod
    def scrape_page_async(self, bookmark: Bookmark):
        """TODO"""


class IndexServiceInterface(abc.ABC):

    @abc.abstractmethod
    def index_page_async(self, page: Page):
        """TODO"""


class SearchServiceInterface(abc.ABC):

    @abc.abstractmethod
    def search_bookmarks(self, query: str, operator: str):
        """TODO"""
