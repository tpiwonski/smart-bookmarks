from django.shortcuts import render, redirect
from django.urls import reverse

from smart_bookmarks.ui.forms import AddBookmarkForm
from smart_bookmarks.core.models import Bookmark
from smart_bookmarks.core.services import BookmarkService


def add_bookmark(request):
    if request.method == 'POST':
        form = AddBookmarkForm(request.POST)
        if form.is_valid():
            bookmark = BookmarkService().add_bookmark(form.cleaned_data['url'])
            return redirect('show-bookmark', guid=bookmark.guid)

    else:
        form = AddBookmarkForm()

    context = {
        'form': form
    }
    return render(request, 'bookmarks/forms/add_bookmark.html', context)


def show_bookmark(request, guid):
    context = {
        'bookmark': Bookmark.objects.by_guid(guid)
    }
    return render(request, "bookmarks/views/show_bookmark.html", context)


def list_bookmarks(request):
    context = {
        'bookmarks': Bookmark.objects.all()
    }
    return render(request, "bookmarks/views/list_bookmarks.html", context)
