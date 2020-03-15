from elasticsearch_dsl import connections, Document, Text, Integer, Q
from smart_bookmarks.core import models
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


class Page(Document):
    bookmark_id = Integer()
    url = Text()
    title = Text()
    description = Text()
    text = Text()

    class Index:
        name = 'smart-bookmarks-page'


class ElasticsearchService:

    def __init__(self, elasticsearch_host):
        connections.create_connection(hosts=[elasticsearch_host])
        Page.init()

    def index_page(self, page: models.Page):
        page_document = Page(
            meta={'id': page.id}, bookmark_id=page.bookmark.id, url=page.bookmark.url, title=page.title,
            description=page.description, text=page.text)
        page_document.save()
        return page_document

    def search_page(self, query, operator):
        search = Page.search().query(
            Q('match', text={
                'query': query,
                # 'fuzziness': 'AUTO',
                'operator': operator.upper() if operator else 'AND'}))
        results = search.execute()
        return results
