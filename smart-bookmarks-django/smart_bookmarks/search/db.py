from django.db import models, transaction


class IndexBookmarkManager(models.Manager):

    @transaction.atomic
    def bookmarks_to_index(self, limit=10):
        index_bookmarks = (
            self.get_queryset().
            select_for_update().
            order_by('id')[:limit])

        bookmarks = [index_bookmark.bookmark for index_bookmark in index_bookmarks]
        self.get_queryset().filter(id__in=index_bookmarks).delete()
        return bookmarks
