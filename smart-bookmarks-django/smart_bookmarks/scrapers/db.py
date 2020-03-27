from django.db import models, transaction
from django.db.models import Q

from smart_bookmarks.core.models import Bookmark, Page


class ScrapePageTaskManager(models.Manager):
    @transaction.atomic
    def bookmarks_to_scrape_in_task(self, limit=10):
        scrape_pages = (
            self.get_queryset().select_for_update().order_by("created")[:limit]
        )

        bookmarks = [scrape_page.bookmark for scrape_page in scrape_pages]
        self.get_queryset().filter(
            id__in=[scrape_page.id for scrape_page in scrape_pages]
        ).delete()
        return bookmarks

    def task_by_bookmark_id(self, bookmark_id):
        try:
            return self.get_queryset().get(bookmark_id=bookmark_id)
        except self.model.DoesNotExist:
            return None

    def bookmarks_not_yet_scraped(self):
        return Bookmark.objects.filter(
            Q(_page__isnull=True)
            & Q(_scrape_page_task__isnull=True)
            & Q(_scrape_page_error__isnull=True)
        ).order_by("id")

    def is_bookmark_scraped(self, bookmark_id):
        return Page.objects.filter(bookmark_id=bookmark_id).exists()
