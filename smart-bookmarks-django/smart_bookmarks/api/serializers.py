from rest_framework import serializers

from smart_bookmarks.core.models import Bookmark, Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["id", "title", "description", "created", "updated"]


class BookmarkSerializer(serializers.ModelSerializer):
    page = PageSerializer()

    class Meta:
        model = Bookmark
        fields = ["id", "guid", "url", "created", "updated", "page"]


class BookmarkSearchHighlightsSerializer(serializers.Serializer):
    url = serializers.ListField(child=serializers.CharField())
    title = serializers.ListField(child=serializers.CharField())
    description = serializers.ListField(child=serializers.CharField())
    text = serializers.ListField(child=serializers.CharField())


class BookmarkSearchResultSerializer(serializers.Serializer):
    score = serializers.FloatField()
    highlights = BookmarkSearchHighlightsSerializer()
    bookmark = BookmarkSerializer()


class BookmarkSearchResultsSerializer(serializers.Serializer):
    total_results = serializers.IntegerField()
    max_score = serializers.FloatField()
    results = BookmarkSearchResultSerializer(many=True)
