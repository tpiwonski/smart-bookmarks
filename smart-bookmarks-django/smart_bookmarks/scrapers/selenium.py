import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumScraperService:

    def __init__(self, chrome_driver_path):
        self._web_driver = None
        self._service = None

        self._service = webdriver.chrome.service.Service(chrome_driver_path)
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

    def scrape_page(self, url):
        self._web_driver.get(url)
        body = self._web_driver.find_element_by_tag_name('html')
        return body.text
