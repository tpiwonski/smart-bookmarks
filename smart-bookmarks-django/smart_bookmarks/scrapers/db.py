from django.db import models, transaction


class ScrapePageManager(models.Manager):

    @transaction.atomic
    def bookmarks_to_scrape(self, limit=10):
        scrape_pages = (
            self.get_queryset().
            select_for_update().
            order_by('created')[:limit])

        bookmarks = [scrape_page.bookmark for scrape_page in scrape_pages]
        self.get_queryset().filter(id__in=[scrape_page.id for scrape_page in scrape_pages]).delete()
        return bookmarks
