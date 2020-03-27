import logging

from smart_bookmarks.core.interfaces import ImportBookmarkInterface
from smart_bookmarks.core.models import Bookmark
from smart_bookmarks.core.registry import get_bookmark_service
from smart_bookmarks.core.utils import url_guid
from smart_bookmarks.importers.netscape import NetscapeBookmarkImportService

LOGGER = logging.getLogger(__name__)


class ImportBookmarkService(ImportBookmarkInterface):
    def __init__(self, bookmark_service=get_bookmark_service):
        self._import_bookmark_service = NetscapeBookmarkImportService()
        self._bookmark_service = bookmark_service()

    def import_file(self, file_path: str):
        bookmarks = self._import_bookmark_service.import_file(file_path)
        for bookmark in bookmarks:
            if not Bookmark.objects.guid_exists(bookmark_guid=url_guid(bookmark.url)):
                self._bookmark_service.create_bookmark(url=bookmark.url)
            else:
                LOGGER.info(f"Bookmark already exists: url={bookmark.url}")
