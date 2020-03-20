import logging

from celery import shared_task, Task

from smart_bookmarks.scrapers.models import ScrapePage
from smart_bookmarks.scrapers.services import ScrapePageService

LOGGER = logging.getLogger(__name__)


class ScrapePageTask(Task):
    _scraper_service = None

    @property
    def scraper_service(self):
        if not self._scraper_service:
            self._scraper_service = ScrapePageService()

        return self._scraper_service


@shared_task(bind=True, base=ScrapePageTask)
def scrape_page(self, bookmark_id):
    if not ScrapePage.objects.bookmark_is_scraped(bookmark_id):
        self.scraper_service.scrape_page_by_id(bookmark_id=bookmark_id)
    else:
        LOGGER.info(f"Bookmark already scrapped: bookmark_id={bookmark_id}")


@shared_task(bind=True)
def scrape_pages(self, limit=10):
    bookmarks = ScrapePage.objects.bookmarks_to_scrape_in_task(limit=limit)
    for bookmark in bookmarks:
        scrape_page.delay(bookmark_id=bookmark.id)
