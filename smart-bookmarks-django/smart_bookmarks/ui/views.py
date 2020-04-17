from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from smart_bookmarks.ui.controllers import BookmarkController
from smart_bookmarks.ui.forms import AddBookmarkForm, SearchBookmarksForm
from smart_bookmarks.ui.utils import ctx


@login_required
def add_bookmark(request):
    if request.method == "POST":
        form = AddBookmarkForm(request.POST)
        if form.is_valid():
            bookmark = BookmarkController().add_bookmark(form.cleaned_data["url"])
            return redirect("show-bookmark", bookmark_guid=bookmark.guid)

    else:
        form = AddBookmarkForm()

    context = {"form": form}
    return render(request, "bookmark/add_bookmark.html", context)


def show_bookmark(request, bookmark_guid):
    return render(
        request,
        "bookmark/show_bookmark.html",
        BookmarkController().get_bookmark(bookmark_guid),
    )


def all_bookmarks(request):
    page_number = request.GET.get("page", 1)
    bookmarks = BookmarkController().all_bookmarks(page_number)
    context = ctx(bookmarks)
    return render(request, "bookmark/bookmarks.html", context)


def search_bookmarks(request):
    page_number = request.GET.get("page", 1)

    form = SearchBookmarksForm(request.GET)
    if form.is_valid() and form.get_query():
        bookmarks = BookmarkController().search_bookmarks(
            query=form.get_query(),
            operator=form.get_operator(),
            page_number=int(page_number),
        )
        context = ctx(bookmarks, form=form)
        return render(request, "search/search.html", context,)
    else:
        form = SearchBookmarksForm()

    context = ctx(form=form)
    return render(request, "search/search.html", context)
