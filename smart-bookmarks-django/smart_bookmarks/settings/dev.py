import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".dev.env", override=True, verbose=True)
from smart_bookmarks.settings.base import *  # noqa isort:skip

CHROME_DRIVER_PATH = os.path.join(BASE_DIR, "..", "bin/chromedriver.exe")  # noqa

ELASTICSEARCH_HOST = "localhost"
