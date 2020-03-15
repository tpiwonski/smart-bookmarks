from dataclasses import dataclass

from bs4 import BeautifulSoup


@dataclass(eq=True, frozen=True)
class Bookmark:
    url: str


class NetscapeBookmarkImportService:

    def import_file(self, file_path):
        parser = NetscapeBookmarksParser()
        with open(file_path, encoding='utf-8') as bookmarks_file:
            return parser.parse_string(bookmarks_file.read())


class NetscapeBookmarksParser:

    def parse_string(self, bookmarks_markup: str):
        bookmarks = set()

        content = BeautifulSoup(bookmarks_markup, features='html.parser')
        bookmark_tags = content.find_all('dt')
        for bookmark_tag in bookmark_tags:
            bookmark_a_tag = bookmark_tag.find('a')
            if not bookmark_a_tag:
                continue

            bookmark_a_href = bookmark_a_tag.attrs.get('href')
            if not (bookmark_a_href
                    and (bookmark_a_href.startswith('http://')
                         or bookmark_a_href.startswith('https://'))):
                continue

            bookmarks.add(Bookmark(url=bookmark_a_href))

        return list(bookmarks)
