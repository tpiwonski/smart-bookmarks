from django.shortcuts import render, redirect

from smart_bookmarks.core.models import Bookmark
from smart_bookmarks.ui.forms import AddBookmarkForm, SearchBookmarksForm
from smart_bookmarks.ui.controllers import SearchController, BookmarkController


def add_bookmark(request):
    if request.method == 'POST':
        form = AddBookmarkForm(request.POST)
        if form.is_valid():
            bookmark = BookmarkController().add_bookmark(form.cleaned_data['url'])
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
        'bookmarks': Bookmark.objects.list_all()
    }
    return render(request, "ui/views/list_bookmarks.html", context)


def search_bookmarks(request):
    # if request.method == 'POST':
    form = SearchBookmarksForm(request.GET)
    if form.is_valid():
        context = {
            'found_bookmarks': SearchController().search_bookmarks(
                query=form.cleaned_data['q'],
                operator=form.cleaned_data['op'])
        }
        return render(request, 'ui/views/search_bookmarks_results.html', context)

    else:
        form = SearchBookmarksForm()

    context = {
        'form': form
    }
    return render(request, 'ui/views/search_bookmarks.html', context)
