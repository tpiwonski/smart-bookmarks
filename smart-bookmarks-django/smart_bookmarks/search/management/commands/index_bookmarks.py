from django.core.management import BaseCommand

from smart_bookmarks.core.registry import get_index_bookmark_service
from smart_bookmarks.search.models import IndexBookmarkTask


class Command(BaseCommand):
    help = 'Index bookmarks'

    def handle(self, *args, **options):
        index_service = get_index_bookmark_service()
        bookmarks = IndexBookmarkTask.objects.bookmarks_not_yet_indexed()
        for bookmark in bookmarks:
            index_service.index_bookmark_async(bookmark)
