from django.core.management import BaseCommand

from smart_bookmarks.core.models import Page
from smart_bookmarks.core.registry import get_index_bookmark_service


class Command(BaseCommand):
    help = 'Index all bookmarks'

    def handle(self, *args, **options):
        index_service = get_index_bookmark_service()
        pages = Page.objects.all()
        for page in pages:
            index_service.index_page(page)
