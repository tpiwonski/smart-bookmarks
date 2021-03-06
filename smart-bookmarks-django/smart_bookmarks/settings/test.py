import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".test.env", override=True, verbose=True)
from smart_bookmarks.settings.base import *  # noqa isort:skip


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),  # noqa
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': os.getenv('DB_NAME'),
    #     'USER': os.getenv('DB_USER'),
    #     'PASSWORD': os.getenv('DB_PASSWORD'),
    #     'HOST': os.getenv('DB_HOST'),
    #     'PORT': os.getenv('DB_PORT'),
    # },
}

CHROME_DRIVER_PATH = os.path.join(BASE_DIR, "..", "bin/chromedriver.exe")  # noqa
