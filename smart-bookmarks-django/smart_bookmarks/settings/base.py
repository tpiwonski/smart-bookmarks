"""
Django settings for smart_bookmarks project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from datetime import timedelta

from celery.schedules import crontab
from kombu import Queue

from smart_bookmarks.authentication.settings import *  # noqa

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5gr+=n9fr=9g=%uc15!r$6rdx1^vh+(nc204orwe3l89m@t4lz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'smart_bookmarks.core',
    'smart_bookmarks.authentication',
    'smart_bookmarks.scrapers',
    'smart_bookmarks.search',
    'smart_bookmarks.ui',
    'smart_bookmarks.importers',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'smart_bookmarks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'smart_bookmarks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'foo': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

CELERY_BROKER_URL = 'pyamqp://{}:{}@{}:{}'.format(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASS'), os.getenv('RABBITMQ_HOST'), os.getenv('RABBITMQ_PORT'))
CELERY_RESULT_BACKEND = 'rpc://' # 'redis://{}:{}'.format(os.getenv('REDIS_HOST'), os.getenv('REDIS_PORT'))
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULE = {
    # 'test-task': {
    #     'task': 'foo.tasks.foo.periodic_task',
    #     'schedule': crontab()
    # },
    'scrape-pages-task': {
        'task': 'smart_bookmarks.scrapers.tasks.scrape_pages',
        'schedule': timedelta(seconds=20)
    },
    'index_pages-task': {
        'task': 'smart_bookmarks.search.tasks.index_pages',
        'schedule': timedelta(seconds=20)
    }
}

CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_QUEUES = (
    Queue('default', routing_key='task.#'),
    Queue('priority', routing_key='priority.#')
)
CELERY_TASK_DEFAULT_EXCHANGE = 'tasks'
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'task.default'

CELERY_TASK_ROUTES = {
    # 'foo.tasks.foo.periodic_task': {
    #     # 'queue': 'default'
    #     'routing_key': 'task.periodic'
    # },
    # 'foo.tasks.foo.simple_task': {
    #     # 'queue': 'priority'
    #     'routing_key': 'priority.simple'
    # },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}/1".format(os.getenv('REDIS_HOST'), os.getenv('REDIS_PORT')),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "example"
    }
}

CACHE_TTL = 20 * 1

PAGE_SERVICE = 'smart_bookmarks.core.services.PageService'
SCRAPER_SERVICE = 'smart_bookmarks.scrapers.services.ScraperService'

CHROME_DRIVER_PATH="/usr/bin/chromedriver"

INDEX_SERVICE = "smart_bookmarks.search.services.IndexService"
SEARCH_SERVICE = 'smart_bookmarks.search.services.SearchService'

ELASTICSEARCH_HOST = 'elasticsearch'
