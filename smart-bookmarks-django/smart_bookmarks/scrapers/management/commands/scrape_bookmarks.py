from django.core.management import BaseCommand

from smart_bookmarks.core.registry import get_scrape_page_service
from smart_bookmarks.scrapers.models import ScrapePage


class Command(BaseCommand):
    help = 'Scrape bookmarks'

    def handle(self, *args, **options):
        scrape_service = get_scrape_page_service()
        bookmarks = ScrapePage.objects.bookmarks_not_yet_scraped()
        for bookmark in bookmarks:
            scrape_service.scrape_page_async(bookmark)
