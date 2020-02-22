import uuid

from celery import shared_task, Task
import logging

LOGGER = logging.getLogger(__name__)


class WebDriverTask(Task):
    _web_driver = None
    _service = None

    @property
    def web_driver(self):
        if self._web_driver:
            return self._web_driver

        import os
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        self._service = webdriver.chrome.service.Service("/usr/bin/chromedriver")
        self._service.start()

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument('--disable-gpu')

        # path to the binary of Chrome Canary that we installed earlier
        # chrome_options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'

        self._web_driver = webdriver.Remote(self._service.service_url, desired_capabilities=chrome_options.to_capabilities())
        return self._web_driver


@shared_task(bind=True, base=WebDriverTask)
def web_driver_task(self):
    LOGGER.info("Run WebDriver based task")

    self.web_driver.get('https://www.ceneo.pl/Telefony_i_akcesoria;szukaj-nokia+3+1+plus')
    body = self.web_driver.find_element_by_tag_name('html')
    LOGGER.info("Page text: %s", body.text)
