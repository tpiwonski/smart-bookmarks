from django.shortcuts import render
from django.views.decorators.http import require_POST, require_http_methods

from smart_bookmarks.ui.controllers import BookmarkController
from smart_bookmarks.ui.templatetags.toast_tags import Toast


@require_POST
def scrape_bookmark(request, bookmark_guid):
    bookmark = BookmarkController().scrape_bookmark(bookmark_guid)
    context = {
        'toasts': [Toast(message=f"Scheduled page {bookmark.url} to scrape", type='info')]
    }
    return render(request, "ui/fragments/ajax_response.html", context)


@require_http_methods(['DELETE'])
def delete_bookmark(request, bookmark_guid):
    # BookmarkController().delete_bookmark(bookmark_guid)
    context = {
        'toasts': [Toast(message=f"Bookmark deleted", type='info')],
    }
    return render(request, "ui/fragments/ajax_response.html", context)
