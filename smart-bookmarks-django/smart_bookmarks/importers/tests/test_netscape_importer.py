import os

from smart_bookmarks.importers.netscape import NetscapeBookmarkImportService

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def test_importer():
    importer = NetscapeBookmarkImportService()
    importer.import_file(os.path.join(FIXTURES_DIR, "bookmarks.html"))
    pass
