from django.db import models, transaction
from django.db.models import F, Q

from smart_bookmarks.core.models import Bookmark


class IndexBookmarkTaskManager(models.Manager):
    @transaction.atomic
    def bookmarks_to_index_in_task(self, limit=None):
        index_bookmarks = self.get_queryset().select_for_update().order_by("id")

        if limit:
            index_bookmarks = index_bookmarks[:limit]

        bookmarks = [index_bookmark.bookmark for index_bookmark in index_bookmarks]
        self.get_queryset().filter(id__in=index_bookmarks).delete()
        return bookmarks

    def task_by_bookmark_id(self, bookmark_id):
        try:
            return self.get_queryset().get(bookmark_id=bookmark_id)
        except self.model.DoesNotExist:
            return None

    def bookmarks_not_yet_indexed(self, limit=None):
        return Bookmark.objects.filter(
            (Q(indexed__isnull=True) | Q(_page__updated__gt=F("indexed")))
            & Q(_index_bookmark_task__isnull=True)
        ).order_by("id")
