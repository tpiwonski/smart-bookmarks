from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from smart_bookmarks.api.serializers import (
    BookmarkSearchResultsSerializer,
    BookmarkSerializer,
)
from smart_bookmarks.core.interfaces import (
    BookmarkSearchResults,
    SearchBookmarkInterface,
)
from smart_bookmarks.core.models import Bookmark
from smart_bookmarks.core.registry import get_search_bookmark_service, inject


class Pagination(PageNumberPagination):
    page_size = 20


class BookmarkViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Bookmark.objects.list_all()
        page = Pagination().paginate_queryset(queryset, request)
        serializer = BookmarkSerializer(page, many=True)
        return Response(serializer.data)


class SearchView(APIView):

    search_service: SearchBookmarkInterface = inject(get_search_bookmark_service)

    def get(self, request):
        query = request.query_params.get("query", "")
        operator = request.query_params.get("op", "and")
        page = int(request.query_params.get("page", 1))

        results = self.search_service.search(query, operator, page, 20)
        results_page = Pagination().paginate_queryset(results, request)

        serializer = BookmarkSearchResultsSerializer(
            BookmarkSearchResults(
                total_results=results.total_results,
                max_score=results.max_score,
                results=results_page,
            )
        )
        return Response(serializer.data)
