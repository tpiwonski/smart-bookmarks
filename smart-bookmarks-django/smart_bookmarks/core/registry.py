from django.conf import settings
from django.utils.module_loading import import_string

from smart_bookmarks.core.interfaces import ScrapeServiceInterface, IndexServiceInterface, SearchServiceInterface


def service_instance(service_path):
    service_class = import_string(service_path)
    return service_class()


def get_bookmark_service():
    from smart_bookmarks.core.services import BookmarkService
    return BookmarkService()


def get_page_service():
    from smart_bookmarks.core.services import PageService
    return PageService()


def get_scrape_service() -> ScrapeServiceInterface:
    return service_instance(settings.SCRAPER_SERVICE)


def get_index_service() -> IndexServiceInterface:
    return service_instance(settings.INDEX_SERVICE)


def get_search_service() -> SearchServiceInterface:
    return service_instance(settings.SEARCH_SERVICE)
