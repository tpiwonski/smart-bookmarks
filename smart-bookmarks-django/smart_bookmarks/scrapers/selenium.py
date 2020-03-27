import logging
from dataclasses import dataclass

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options

LOGGER = logging.getLogger(__name__)


class ScrapeError(Exception):
    def __init__(self, message):
        self.message = message


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

        try:
            self._service = webdriver.chrome.service.Service(self.chrome_driver_path)
            self._service.start()

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("window-size=1920,1080")
            chrome_options.add_argument("--disable-gpu")

            # path to the binary of Chrome Canary that we installed earlier
            # chrome_options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'

            self._web_driver = webdriver.Remote(
                self._service.service_url,
                desired_capabilities=chrome_options.to_capabilities(),
            )
        except Exception as ex:
            LOGGER.exception(ex)
            raise ScrapeError(f"Init driver error: error={str(ex)}")

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
        try:
            requests.get(url)
        except Exception as ex:
            LOGGER.exception(ex)
            raise ScrapeError(f"Error occurred when requesting URL: error={str(ex)}")

        if self._web_driver is None:
            self.init_driver()

        for timeout in (30, 60, 120):
            try:
                LOGGER.info(f"Scrape page: url={url} timeout={timeout}")
                return self.parse_page(url, timeout)
            except ScrapeError:
                raise
            except WebDriverException as ex:
                LOGGER.exception(ex)
                self.dispose_driver()
            except Exception as ex:
                LOGGER.exception(ex)

        self.dispose_driver()
        raise ScrapeError(f"Unable to scrape page")

    def parse_page(self, url, timeout) -> PageData:
        self._web_driver.implicitly_wait(timeout)
        self._web_driver.get(url)
        # sleep(timeout)

        title = self._web_driver.title
        source = self._web_driver.page_source
        html_tag = self._web_driver.find_element_by_tag_name("html")
        text = html_tag.text
        if not text:
            raise ScrapeError(f"No text available for page")

        try:
            description_tag = self._web_driver.find_element_by_xpath(
                "//meta[@name='description']"
            )
        except NoSuchElementException:
            description = None
        else:
            description = description_tag.get_attribute("content")

        return PageData(title=title, description=description, text=text, source=source)
