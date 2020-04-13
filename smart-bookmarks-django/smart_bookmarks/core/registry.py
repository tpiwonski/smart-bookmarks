from django.conf import settings
from django.utils.functional import cached_property
from django.utils.module_loading import import_string

from smart_bookmarks.core.interfaces import (
    CreateBookmarkInterface,
    CreatePageInterface,
    ImportBookmarkInterface,
    IndexBookmarkInterface,
    ScrapePageInterface,
    SearchBookmarkInterface,
)


def service_instance(service_path):
    service_class = import_string(service_path)
    return service_class()


def inject(service_factory):
    return cached_property(lambda _: service_factory())


def get_bookmark_service() -> CreateBookmarkInterface:
    return service_instance(settings.BOOKMARK_SERVICE)


def get_page_service() -> CreatePageInterface:
    return service_instance(settings.PAGE_SERVICE)


def get_scrape_page_service() -> ScrapePageInterface:
    return service_instance(settings.SCRAPE_PAGE_SERVICE)


def get_index_bookmark_service() -> IndexBookmarkInterface:
    return service_instance(settings.INDEX_BOOKMARK_SERVICE)


def get_search_bookmark_service() -> SearchBookmarkInterface:
    return service_instance(settings.SEARCH_BOOKMARK_SERVICE)


def get_import_bookmark_service() -> ImportBookmarkInterface:
    return service_instance(settings.IMPORT_BOOKMARK_SERVICE)
