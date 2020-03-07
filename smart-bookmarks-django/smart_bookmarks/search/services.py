from django.conf import settings

from smart_bookmarks.search.elasticsearch import ElasticsearchService


class SearchService:

    def __init__(self):
        self._search_service = ElasticsearchService(settings.ELASTICSEARCH_HOST)

    def index_page(self, page):
        self._search_service.index_page(page)

    def search_page(self, term):
        return self._search_service.search_page(term)
