from django.core.management import BaseCommand

from smart_bookmarks.core.models import Bookmark
from smart_bookmarks.core.registry import get_scrape_page_service


class Command(BaseCommand):
    help = 'Scrape bookmarks'

    def handle(self, *args, **options):
        scrape_service = get_scrape_page_service()
        bookmarks = Bookmark.objects.bookmarks_to_scrape()
        for bookmark in bookmarks:
            scrape_service.scrape_page_async(bookmark)
