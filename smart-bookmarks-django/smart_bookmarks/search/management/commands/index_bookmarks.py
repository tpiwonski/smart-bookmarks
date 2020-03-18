from django.core.management import BaseCommand

from smart_bookmarks.core.models import Bookmark
from smart_bookmarks.core.registry import get_index_bookmark_service


class Command(BaseCommand):
    help = 'Index bookmarks'

    def handle(self, *args, **options):
        index_service = get_index_bookmark_service()
        bookmarks = Bookmark.objects.bookmarks_to_index()
        for bookmark in bookmarks:
            index_service.index_bookmark_async(bookmark)
