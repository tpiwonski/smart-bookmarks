from django.core.management import BaseCommand

from smart_bookmarks.core.registry import get_import_bookmark_service


class Command(BaseCommand):
    help = 'Import bookmarks from the specified file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='A path to the bookmarks file')

    def handle(self, *args, **options):
        import_service = get_import_bookmark_service()
        import_service.import_file(options['file'])
