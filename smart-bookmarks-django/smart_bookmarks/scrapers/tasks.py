import logging

from celery import shared_task, Task

from smart_bookmarks.scrapers.models import ScrapePage
from smart_bookmarks.scrapers.services import ScraperService

LOGGER = logging.getLogger(__name__)


class ScrapePageTask(Task):
    _scraper_service = None

    @property
    def scraper_service(self):
        if not self._scraper_service:
            self._scraper_service = ScraperService()

        return self._scraper_service


@shared_task(bind=True, base=ScrapePageTask)
def scrape_page(self, bookmark_id):
    self.scraper_service.scrape_page_by_id(bookmark_id=bookmark_id)


@shared_task(bind=True)
def scrape_pages(self):
    bookmarks = ScrapePage.objects.bookmarks_to_scrape()
    for bookmark in bookmarks:
        scrape_page.delay(bookmark_id=bookmark.id)
