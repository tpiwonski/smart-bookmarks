from django.db import models

# Create your models here.
from smart_bookmarks.search.db import IndexBookmarkManager


class IndexBookmark(models.Model):
    id = models.AutoField(primary_key=True)
    bookmark = models.OneToOneField('core.Bookmark', on_delete=models.CASCADE, related_name='_index_bookmark')
    created = models.DateTimeField(auto_now_add=True)

    objects = IndexBookmarkManager()

    class Meta:
        db_table = 'index_bookmark'
        constraints = [
            models.UniqueConstraint(fields=['bookmark'], name='uq_bookmark_id')]
