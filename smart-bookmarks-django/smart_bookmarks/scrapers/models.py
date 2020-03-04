from django.db import models

from smart_bookmarks.scrapers.db import ScrapePageManager


class ScrapePage(models.Model):
    id = models.AutoField(primary_key=True)
    bookmark = models.OneToOneField('bookmarks.Bookmark', on_delete=models.CASCADE, related_name='scrape_pages')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ScrapePageManager()

    class Meta:
        db_table = 'scrape_page'
