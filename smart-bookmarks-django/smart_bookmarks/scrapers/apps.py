from django.apps import AppConfig


class ScrapersConfig(AppConfig):
    name = 'smart_bookmarks.scrapers'

    def ready(self):
        from smart_bookmarks.scrapers.receivers import on_bookmark_created  # noqa
