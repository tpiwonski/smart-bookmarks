from django.shortcuts import redirect, render

from smart_bookmarks.ui.controllers import BookmarkController, SearchController
from smart_bookmarks.ui.forms import AddBookmarkForm, SearchBookmarksForm


def add_bookmark(request):
    if request.method == 'POST':
        form = AddBookmarkForm(request.POST)
        if form.is_valid():
            bookmark = BookmarkController().add_bookmark(form.cleaned_data['url'])
            return redirect('show-bookmark', bookmark_guid=bookmark.guid)

    else:
        form = AddBookmarkForm()

    context = {
        'form': form
    }
    return render(request, 'ui/views/add_bookmark.html', context)


def show_bookmark(request, bookmark_guid):
    return render(
        request, "ui/views/show_bookmark.html",
        BookmarkController().get_bookmark(bookmark_guid))


def list_bookmarks(request):
    return render(
        request, "ui/views/list_bookmarks.html",
        BookmarkController().list_bookmarks())


def search_bookmarks(request):
    # if request.method == 'POST':
    form = SearchBookmarksForm(request.GET)
    if form.is_valid():
        return render(
            request, 'ui/views/search_bookmarks_results.html',
            SearchController().search_bookmarks(
                query=form.cleaned_data['q'],
                operator=form.cleaned_data['op']))

    else:
        form = SearchBookmarksForm()

    context = {
        'form': form
    }
    return render(request, 'ui/views/search_bookmarks.html', context)
