import functools
import operator as op
from dataclasses import dataclass

from elasticsearch_dsl import Document, Q, Text, connections

from smart_bookmarks.core import models

SEARCH_OPERATOR_AND = "AND"
SEARCH_OPERATOR_OR = "OR"
SEARCH_OPERATORS = (SEARCH_OPERATOR_AND, SEARCH_OPERATOR_OR)

SEARCH_FIELDS = ("url", "title", "description", "text")


@dataclass
class BookmarkData:
    id: int
    url: str
    title: str
    description: str
    text: str


class BookmarkDocument(Document):
    url = Text()
    title = Text()
    description = Text()
    text = Text()

    class Index:
        name = "smart-bookmarks-bookmark"


class ElasticsearchService:
    def __init__(self, elasticsearch_host):
        connections.create_connection(hosts=[elasticsearch_host])
        BookmarkDocument.init()

    def index_bookmark(self, bookmark_data: BookmarkData):
        bookmark_document = BookmarkDocument(
            meta={"id": bookmark_data.id},
            url=bookmark_data.url,
            title=bookmark_data.title,
            description=bookmark_data.description,
            text=bookmark_data.text,
        )
        bookmark_document.save()
        return bookmark_document

    def search_bookmark(self, query, operator):
        search_operator = operator.upper()
        if search_operator not in SEARCH_OPERATORS:
            raise Exception(f"Unknown search operator {operator}")

        search_queries = [
            Q("match", **{field: {"query": query, "operator": search_operator}})
            for field in SEARCH_FIELDS
        ]

        search_query = functools.reduce(op.or_, search_queries)
        search = BookmarkDocument.search().query(search_query).highlight(*SEARCH_FIELDS)

        # q = Q('multi_match', query=query, fields=['url', 'title', 'description', 'text'])
        # Q('match', text={
        #     'query': query,
        #     # 'fuzziness': 'AUTO',
        #     'operator': operator.upper() if operator else 'AND'}))

        results = search.execute()
        return results
