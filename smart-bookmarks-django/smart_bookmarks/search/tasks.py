from celery import shared_task

from smart_bookmarks.search.models import IndexBookmark
from smart_bookmarks.search.services import IndexBookmarkService


@shared_task(bind=True)
def index_bookmarks(self):
    bookmarks = IndexBookmark.objects.bookmarks_to_index()
    for bookmark in bookmarks:
        index_bookmark.delay(bookmark_id=bookmark.id)


@shared_task(bind=True)
def index_bookmark(self, bookmark_id):
    IndexBookmarkService().index_bookmark_by_id(bookmark_id)
