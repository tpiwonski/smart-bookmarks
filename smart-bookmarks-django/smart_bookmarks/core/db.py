from django.db import models
from django.db.models import Q, F


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

    def bookmarks_to_index(self):
        return self.get_queryset().filter(Q(indexed__isnull=True) | Q(_page__updated__gt=F('indexed'))).order_by('id')

    def bookmarks_to_scrape(self):
        return self.get_queryset().filter(_page__isnull=True).order_by('id')


class PageManager(models.Manager):

    def by_id(self, page_id):
        return self.get_queryset().get(id=page_id)
