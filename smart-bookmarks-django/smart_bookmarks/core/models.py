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

    def __str__(self):
        return f"Bookmark#{self.id}:url={self.url}"


class Page(models.Model):
    id = models.AutoField(primary_key=True)
    bookmark = models.OneToOneField(Bookmark, on_delete=models.CASCADE, related_name='page')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    text = models.TextField()
    source = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = PageManager()

    class Meta:
        db_table = 'page'

    def __str__(self):
        return f"Page#{self.id}:bookmark={self.bookmark}"
