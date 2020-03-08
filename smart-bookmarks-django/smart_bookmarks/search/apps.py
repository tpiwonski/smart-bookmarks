from django.apps import AppConfig


class SearchConfig(AppConfig):
    name = 'smart_bookmarks.search'

    def ready(self):
        from smart_bookmarks.search.receivers import on_page_created  # noqa
