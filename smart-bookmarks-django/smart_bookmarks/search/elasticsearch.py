from elasticsearch_dsl import connections, Document, Text
from smart_bookmarks.core import models
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


class Page(Document):
    text = Text()

    class Index:
        name = 'smart-bookmarks-page'


class ElasticsearchService:

    def __init__(self, elasticsearch_host):
        connections.create_connection(hosts=[elasticsearch_host])
        Page.init()

    def index_page(self, page: models.Page):
        page_document = Page(meta={'id': page.id}, text=page.text)
        page_document.save()

    def search_page(self, term):
        search = Page.search().query('match', text=term)
        results = search.execute()
        return results
