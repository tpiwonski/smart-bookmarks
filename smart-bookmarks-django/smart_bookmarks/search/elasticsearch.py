from dataclasses import dataclass

from elasticsearch import Elasticsearch

SEARCH_OPERATOR_AND = "AND"
SEARCH_OPERATOR_OR = "OR"
SEARCH_OPERATORS = (SEARCH_OPERATOR_AND, SEARCH_OPERATOR_OR)

SEARCH_FIELDS = ("url", "title^3", "description^2", "text")

BOOKMARK_INDEX = "smart-bookmarks-bookmark"


@dataclass
class BookmarkData:
    id: int
    url: str
    title: str
    description: str
    text: str


class ElasticsearchService:
    def __init__(self, elasticsearch_host):
        self.elasticsearch = Elasticsearch(hosts=[elasticsearch_host])
        self._create_index()

    def _create_index(self):
        self.elasticsearch.indices.create(
            index=BOOKMARK_INDEX,
            body={
                "mappings": {
                    "properties": {
                        "url": {"type": "text"},
                        "title": {"type": "text"},
                        "description": {"type": "text"},
                        "text": {"type": "text"},
                    }
                }
            },
            ignore=[400],
        )

    def index_bookmark(self, bookmark_data: BookmarkData):
        self.elasticsearch.index(
            index=BOOKMARK_INDEX,
            id=bookmark_data.id,
            body={
                "url": bookmark_data.url,
                "title": bookmark_data.title,
                "description": bookmark_data.description,
                "text": bookmark_data.text,
            },
        )

    def search_bookmark(self, query, operator, offset=None, limit=None):
        search_operator = operator.upper()
        if search_operator not in SEARCH_OPERATORS:
            raise Exception(f"Unknown search operator {operator}")

        search_query = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                field: {"query": query, "operator": search_operator}
                            }
                        }
                        for field in SEARCH_FIELDS
                    ]
                }
            }
        }
        search_highlight = {
            "highlight": {
                "fields": {"url": {}, "title": {}, "description": {}, "text": {}}
            }
        }
        search_pagination = {}
        if offset:
            search_pagination["from"] = offset
        if limit:
            search_pagination["size"] = limit

        search_body = {**search_query, **search_highlight, **search_pagination}
        search_results = self.elasticsearch.search(
            index=BOOKMARK_INDEX, body=search_body
        )
        return search_results
