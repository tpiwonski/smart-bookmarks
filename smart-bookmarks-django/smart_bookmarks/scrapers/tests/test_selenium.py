from django.conf import settings

from smart_bookmarks.scrapers.selenium import SeleniumScrapePageService

from requests import Session

# def test_selenium():
#     scrape_page_service = SeleniumScrapePageService(settings.CHROME_DRIVER_PATH)
#     page_data = scrape_page_service.scrape_page('https://developers.facebook.com/docs/marketing-api/audiences-api/pixel')
#     pass


def test_requests():
    s = Session()
    try:
        # r = s.get("https://www.dsync.com/")
        # r = s.get("https://blog.wearewizards.io/a-mobx-introduction-and-case-study")
        r = s.get("https://onet.pl")
    except Exception as ex:
        pass
    pass
