import logging

from django.conf import settings

from smart_bookmarks.core.interfaces import ScrapeServiceInterface
from smart_bookmarks.core.models import Bookmark
from smart_bookmarks.core.registry import get_page_service
from smart_bookmarks.scrapers.selenium import SeleniumScraperService
from smart_bookmarks.scrapers.models import ScrapePage

LOGGER = logging.getLogger(__name__)


class ScraperService(ScrapeServiceInterface):

    def __init__(self, page_service=get_page_service):
        self._scraper_service = SeleniumScraperService(settings.CHROME_DRIVER_PATH)
        self._page_service = page_service()

    def scrape_page_async(self, bookmark):
        scrape_page = ScrapePage.objects.create(bookmark=bookmark)
        LOGGER.info("Scrape page created: scrape_page_id=%s, bookmark_id=%s", scrape_page.id, bookmark.id)

    def scrape_page_by_id(self, bookmark_id):
        try:
            bookmark = Bookmark.objects.by_id(bookmark_id)
        except Bookmark.DoesNotExist:
            LOGGER.info("Bookmark does not exist: bookmark_id=%s", bookmark_id)
            return None

        page = self.scrape_page(bookmark)
        return page

    def scrape_page(self, bookmark):
        LOGGER.info("Scrape page for bookmark: bookmark_id=%s", bookmark.id)
        scraped_content = self._scraper_service.scrape_page(bookmark.url)
        page = self._page_service.create_page(bookmark, scraped_content)
        LOGGER.info(
            "Page scraped for bookmark: page_id=%s, bookmark_id=%s", page.id, bookmark.id)
        return page
