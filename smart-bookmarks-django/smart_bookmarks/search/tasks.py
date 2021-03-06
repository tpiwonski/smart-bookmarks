from celery import shared_task

from smart_bookmarks.search.models import IndexBookmarkTask
from smart_bookmarks.search.services import IndexBookmarkService


@shared_task(bind=True)
def index_bookmarks(self, limit=10):
    bookmarks = IndexBookmarkTask.objects.bookmarks_to_index_in_task(limit=None)
    for bookmark in bookmarks:
        index_bookmark.delay(bookmark_id=bookmark.id)


@shared_task(bind=True)
def index_bookmark(self, bookmark_id):
    IndexBookmarkService().index_bookmark_by_id(bookmark_id)
