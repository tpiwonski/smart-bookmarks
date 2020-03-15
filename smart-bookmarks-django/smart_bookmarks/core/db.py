from django.db import models


class BookmarkManager(models.Manager):

    def by_id(self, bookmark_id):
        try:
            return self.get_queryset().get(id=bookmark_id)
        except self.model.DoesNotExist:
            return None

    def by_guid(self, bookmark_guid):
        try:
            return self.get_queryset().get(guid=bookmark_guid)
        except self.model.DoesNotExist:
            return None

    def by_page_ids(self, page_ids):
        return self.get_queryset().filter(page__in=page_ids)

    def guid_exists(self, bookmark_guid):
        return self.get_queryset().filter(guid=bookmark_guid).exists()


class PageManager(models.Manager):

    def by_id(self, page_id):
        return self.get_queryset().get(id=page_id)
