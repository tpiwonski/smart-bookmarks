from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_POST

from smart_bookmarks.ui.controllers import BookmarkController


@require_POST
def scrape_bookmark(request, bookmark_guid):
    context = BookmarkController().scrape_bookmark(bookmark_guid)
    for message in context["messages"]:
        messages.add_message(request, message.level, message.message)

    return render(request, "ajax_response.html", context)


@require_http_methods(["DELETE"])
def delete_bookmark(request, bookmark_guid):
    context = BookmarkController().delete_bookmark(bookmark_guid)
    for message in context["messages"]:
        messages.add_message(request, message.level, message.message)

    return render(request, "ajax_response.html", context)
