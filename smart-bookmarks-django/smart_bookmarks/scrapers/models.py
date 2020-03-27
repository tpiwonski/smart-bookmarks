from django.db import models

from smart_bookmarks.scrapers.db import ScrapePageTaskManager


class ScrapePageTask(models.Model):
    id = models.AutoField(primary_key=True)
    bookmark = models.OneToOneField(
        "core.Bookmark", on_delete=models.CASCADE, related_name="_scrape_page_task"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ScrapePageTaskManager()

    class Meta:
        db_table = "scrape_page_task"
        constraints = [
            models.UniqueConstraint(
                fields=["bookmark"], name="uq_scrape_page_task_bookmark_id"
            )
        ]


class ScrapePageError(models.Model):
    id = models.AutoField(primary_key=True)
    bookmark = models.OneToOneField(
        "core.Bookmark", on_delete=models.CASCADE, related_name="_scrape_page_error"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=1024)

    class Meta:
        db_table = "scrape_page_error"
