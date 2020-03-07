from django.db import models

from smart_bookmarks.core.db import BookmarkManager, PageManager


class Bookmark(models.Model):
    id = models.AutoField(primary_key=True)
    guid = models.CharField(max_length=64)
    url = models.URLField(max_length=2048)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = BookmarkManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['guid'], name='uq_bookmark_quid')]
        db_table = 'bookmark'

    @property
    def last_page(self):
        return self.pages.latest('updated')


class Page(models.Model):
    id = models.AutoField(primary_key=True)
    bookmark = models.ForeignKey(Bookmark, on_delete=models.CASCADE, related_name='pages')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = PageManager()

    class Meta:
        db_table = 'page'
