from django.conf import settings

from smart_bookmarks.scrapers.selenium import SeleniumScrapePageService


def test_selenium():
    scrape_page_service = SeleniumScrapePageService(settings.CHROME_DRIVER_PATH)
    page_data = scrape_page_service.scrape_page('https://github.com/paddle8/runbooks/wiki/Development-Environment')
    pass
