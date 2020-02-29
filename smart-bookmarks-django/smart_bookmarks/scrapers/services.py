import logging

from smart_bookmarks.bookmarks.models import Bookmark, Page
from smart_bookmarks.scrapers.integrations.selenium import SeleniumScraperService
from smart_bookmarks.scrapers.models import ScrapePageTask

LOGGER = logging.getLogger(__name__)


class ScraperService:

    def __init__(self):
        self._scraper_service = SeleniumScraperService()

    def enqueue_scrape_page_task(self, bookmark):
        task = ScrapePageTask.objects.create(bookmark=bookmark)
        LOGGER.info("Scrape page task created: task_id=%s, bookmark_id=%s", task.id, bookmark.id)

    def process_scrape_page_task(self, task_id):
        LOGGER.info("Process scrape page task: task_id=%s", task_id)
        task = ScrapePageTask.objects.get(id=task_id)
        try:
            page = self.scrape_page(task.bookmark)
            LOGGER.info(
                "Page scraped for bookmark: task_id=%s, page_id=%s, bookmark_id=%s",
                task.id, page.id, task.bookmark.id)
        except Exception as ex:
            LOGGER.exception(
                "An error occurred while scraping page: task_id=%s, bookmark_id=%s", task.id, task.bookmark.id)
            task.update_state(ScrapePageTask.STATE_FAILED)
        else:
            task.delete()

    def scrape_page(self, bookmark):
        LOGGER.info("Scrape page for bookmark: bookmark_id=%s", bookmark.id)
        scraped_content = self._scraper_service.scrape_page(bookmark.url)
        return Page.objects.create(bookmark=bookmark, text=scraped_content)
