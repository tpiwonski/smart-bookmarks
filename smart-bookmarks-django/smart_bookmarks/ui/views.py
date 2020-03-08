from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse

from smart_bookmarks.core.utils import service_instance
from smart_bookmarks.ui.forms import AddBookmarkForm, SearchBookmarksForm
from smart_bookmarks.core.models import Bookmark
from smart_bookmarks.core.services import BookmarkService


def add_bookmark(request):
    if request.method == 'POST':
        form = AddBookmarkForm(request.POST)
        if form.is_valid():
            bookmark = BookmarkService().create_bookmark(form.cleaned_data['url'])
            return redirect('show-bookmark', guid=bookmark.guid)

    else:
        form = AddBookmarkForm()

    context = {
        'form': form
    }
    return render(request, 'ui/views/add_bookmark.html', context)


def show_bookmark(request, guid):
    context = {
        'bookmark': Bookmark.objects.by_guid(guid)
    }
    return render(request, "ui/views/show_bookmark.html", context)


def list_bookmarks(request):
    context = {
        'bookmarks': Bookmark.objects.all()
    }
    return render(request, "ui/views/list_bookmarks.html", context)


def search_bookmarks(request):
    if request.method == 'POST':
        form = SearchBookmarksForm(request.POST)
        if form.is_valid():
            search_service = service_instance(settings.SEARCH_SERVICE)
            context = {
                'bookmarks': search_service.search_bookmarks(form.cleaned_data['q'])
            }
            return render(request, 'ui/views/list_bookmarks.html', context)

    else:
        form = SearchBookmarksForm()

    context = {
        'form': form
    }
    return render(request, 'ui/forms/add_bookmark.html', context)
