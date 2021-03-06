from typing import List

from django.db import models
from django.db.models import F, Q


class BookmarkManager(models.Manager):
    def by_id(self, bookmark_id):
        try:
            return self.get_queryset().get(id=bookmark_id)
        except self.model.DoesNotExist:
            return None

    def by_ids(self, bookmark_ids: List[int]):
        return self.get_queryset().filter(id__in=bookmark_ids)

    def by_guid(self, bookmark_guid):
        try:
            return self.get_queryset().get(guid=bookmark_guid)
        except self.model.DoesNotExist:
            return None

    def by_page_ids(self, page_ids):
        return self.get_queryset().filter(page__in=page_ids)

    def guid_exists(self, bookmark_guid):
        return self.get_queryset().filter(guid=bookmark_guid).exists()

    def list_all(self):
        return self.get_queryset().all().select_related("_page")

    def delete_by_guid(self, bookmark_guid):
        return self.get_queryset().filter(guid=bookmark_guid).delete()


class PageManager(models.Manager):
    def by_id(self, page_id):
        return self.get_queryset().get(id=page_id)

    def by_bookmark_id(self, bookmark_id):
        try:
            return self.get_queryset().get(bookmark_id=bookmark_id)
        except self.model.DoesNotExist:
            return None
