from django.db import models


class BookmarkManager(models.Manager):

    def by_id(self, bookmark_id):
        return self.get_queryset().get(id=bookmark_id)

    def by_guid(self, bookmark_guid):
        return self.get_queryset().get(guid=bookmark_guid)

    def by_page_ids(self, page_ids):
        return self.get_queryset().filter(page__in=page_ids)


class PageManager(models.Manager):

    def by_id(self, page_id):
        return self.get_queryset().get(id=page_id)
