import logging

from django.conf import settings

from smart_bookmarks.core.interfaces import ScrapePageInterface, PageData, CreatePageInterface
from smart_bookmarks.core.models import Bookmark
from smart_bookmarks.core.registry import get_page_service, inject
from smart_bookmarks.scrapers.models import ScrapePage
from smart_bookmarks.scrapers.selenium import SeleniumScrapePageService

LOGGER = logging.getLogger(__name__)


class ScrapePageService(ScrapePageInterface):

    scrape_page_service: SeleniumScrapePageService = inject(
        lambda: SeleniumScrapePageService(settings.CHROME_DRIVER_PATH))
    page_service: CreatePageInterface = inject(get_page_service)

    def scrape_page_async(self, bookmark):
        scrape_page = ScrapePage.objects.by_bookmark_id(bookmark.id)
        if not scrape_page:
            scrape_page = ScrapePage.objects.create(bookmark=bookmark)

        LOGGER.info("Scrape page created: scrape_page_id=%s, bookmark_id=%s", scrape_page.id, bookmark.id)

    def scrape_page_by_id(self, bookmark_id):
        bookmark = Bookmark.objects.by_id(bookmark_id)
        if bookmark is None:
            LOGGER.info("Bookmark does not exist: bookmark_id=%s", bookmark_id)
            return None

        page = self.scrape_page(bookmark)
        return page

    def scrape_page(self, bookmark):
        LOGGER.info("Scrape page for bookmark: bookmark_id=%s", bookmark.id)
        scraped_data = self.scrape_page_service.scrape_page(bookmark.url)
        page_data = PageData(
            title=scraped_data.title if scraped_data.title else scraped_data.text[:255].title,
            description=scraped_data.description[:1024] if scraped_data.description else scraped_data.text[:1024],
            text=scraped_data.text,
            source=scraped_data.source)
        page = self.page_service.create_page(bookmark, page_data)
        LOGGER.info(
            "Page scraped for bookmark: page_id=%s, bookmark_id=%s", page.id, bookmark.id)
        return page
