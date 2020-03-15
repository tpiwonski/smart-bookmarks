import logging
from dataclasses import dataclass
from time import sleep
from typing import List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

LOGGER = logging.getLogger(__name__)


@dataclass
class PageData:
    title: str
    description: str
    text: str
    source: str


class SeleniumScrapePageService:

    def __init__(self, chrome_driver_path):
        self.chrome_driver_path = chrome_driver_path
        self.init_driver()

    def init_driver(self):
        LOGGER.info("Init web driver")
        self._web_driver = None
        self._service = None

        self._service = webdriver.chrome.service.Service(self.chrome_driver_path)
        self._service.start()

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument('--disable-gpu')

        # path to the binary of Chrome Canary that we installed earlier
        # chrome_options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'

        self._web_driver = webdriver.Remote(
            self._service.service_url, desired_capabilities=chrome_options.to_capabilities())
        self._web_driver.implicitly_wait(10)

    def dispose_driver(self):
        LOGGER.info("Dispose web driver")
        try:
            self._web_driver.quit()
        except Exception as ex:
            LOGGER.exception(ex)

        try:
            self._service.stop()
        except Exception as ex:
            LOGGER.exception(ex)

        self._web_driver = None
        self._service = None

    def scrape_page(self, url) -> PageData:
        if self._web_driver is None:
            self.init_driver()

        for timeout in (1, 3, 5, 10, 15):
            try:
                LOGGER.info(f"Scrape page: url={url} timeout={timeout}")
                return self.parse_page(url, timeout)
            except Exception as ex:
                LOGGER.exception(ex)

        self.dispose_driver()
        raise Exception(f"Failed to scrape page: url={url}")

    def parse_page(self, url, timeout) -> PageData:
        self._web_driver.get(url)
        sleep(timeout)
        title = self._web_driver.title
        source = self._web_driver.page_source
        html_tag = self._web_driver.find_element_by_tag_name('html')
        text = html_tag.text
        if not text:
            raise Exception(f"No text scraped for page: url={url}")

        try:
            description_tag = self._web_driver.find_element_by_xpath("//meta[@name='description']")
        except NoSuchElementException:
            description = None
        else:
            description = description_tag.get_attribute('content')

        return PageData(title=title, description=description, text=text, source=source)
