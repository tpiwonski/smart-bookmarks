import functools
import operator as op

from elasticsearch_dsl import connections, Document, Text, Integer, Q
from smart_bookmarks.core import models
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

SEARCH_OPERATOR_AND = 'AND'
SEARCH_OPERATOR_OR = 'OR'
SEARCH_OPERATORS = (SEARCH_OPERATOR_AND, SEARCH_OPERATOR_OR)

SEARCH_FIELDS = ('url', 'title', 'description', 'text')


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
        search_operator = operator.upper()
        if search_operator not in SEARCH_OPERATORS:
            raise Exception(f"Unknown search operator {o}")

        search_queries = [
            Q('match',
              **{field: {
                  'query': query,
                  'operator': search_operator}})
            for field in SEARCH_FIELDS]

        search_query = functools.reduce(op.or_, search_queries)
        search = Page.search().query(search_query).highlight(*SEARCH_FIELDS)

        # q = Q('multi_match', query=query, fields=['url', 'title', 'description', 'text'])
            # Q('match', text={
            #     'query': query,
            #     # 'fuzziness': 'AUTO',
            #     'operator': operator.upper() if operator else 'AND'}))

        results = search.execute()
        return results
