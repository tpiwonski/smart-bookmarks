from django.db import models


class BookmarkManager(models.Manager):

    def by_id(self, bookmark_id):
        return self.get_queryset().get(id=bookmark_id)

    def by_guid(self, bookmark_guid):
        return self.get_queryset().get(guid=bookmark_guid)


class PageManager(models.Manager):
    pass
