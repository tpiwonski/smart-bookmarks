from django.shortcuts import redirect, render

from smart_bookmarks.ui.controllers import BookmarkController, SearchController
from smart_bookmarks.ui.forms import AddBookmarkForm, SearchBookmarksForm
from smart_bookmarks.ui.utils import ViewInfo


def add_bookmark(request):
    if request.method == "POST":
        form = AddBookmarkForm(request.POST)
        if form.is_valid():
            bookmark = BookmarkController().add_bookmark(form.cleaned_data["url"])
            return redirect("show-bookmark", bookmark_guid=bookmark.guid)

    else:
        form = AddBookmarkForm()

    context = {"form": form}
    return render(request, "ui/views/add_bookmark.html", context)


def show_bookmark(request, bookmark_guid):
    return render(
        request,
        "ui/views/show_bookmark.html",
        BookmarkController().get_bookmark(bookmark_guid),
    )


def list_bookmarks(request):
    page_number = request.GET.get("page", 1)
    context = {
        **BookmarkController().list_bookmarks(page_number),
        **{
            "view": ViewInfo("list-bookmarks")
        }
    }
    return render(
        request,
        "ui/views/list_bookmarks.html",
        context
    )


def search_bookmarks(request):
    page_number = request.GET.get("page", 1)
    form = SearchBookmarksForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data["q"]
        operator = form.cleaned_data["op"]
        context = {
            **SearchController().search_bookmarks(
                query=query,
                operator=operator,
                page_number=int(page_number),
            ),
            **{
                "search_view": ViewInfo("search-bookmarks", query={"q": query, "op": operator})
            }
        }
        return render(
            request,
            "ui/views/search_bookmarks_results.html",
            context,
        )

    else:
        form = SearchBookmarksForm()

    context = {"form": form}
    return render(request, "ui/views/search_bookmarks.html", context)
