from django.shortcuts import render
from django.views.decorators.http import require_POST, require_http_methods

from smart_bookmarks.ui.controllers import BookmarkController


@require_POST
def scrape_bookmark(request, bookmark_guid):
    return render(
        request, "ui/fragments/ajax_response.html",
        BookmarkController().scrape_bookmark(bookmark_guid))


@require_http_methods(['DELETE'])
def delete_bookmark(request, bookmark_guid):
    return render(
        request, "ui/fragments/ajax_response.html",
        BookmarkController().delete_bookmark(bookmark_guid))
