from django.db import models

# Create your models here.
from smart_bookmarks.search.db import IndexBookmarkTaskManager


class IndexBookmarkTask(models.Model):
    id = models.AutoField(primary_key=True)
    bookmark = models.OneToOneField('core.Bookmark', on_delete=models.CASCADE, related_name='_index_bookmark_task')
    created = models.DateTimeField(auto_now_add=True)

    objects = IndexBookmarkTaskManager()

    class Meta:
        db_table = 'index_bookmark_task'
        constraints = [
            models.UniqueConstraint(fields=['bookmark'], name='uq_index_bookmark_task_bookmark_id')]
