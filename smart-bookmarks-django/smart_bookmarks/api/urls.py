from django.urls import include, path

from rest_framework import routers

from smart_bookmarks.api.views import BookmarkViewSet, SearchView

router = routers.DefaultRouter()
router.register(r"bookmarks", BookmarkViewSet, basename="bookmark")

urlpatterns = [path("", include(router.urls)), path(r"search/", SearchView.as_view())]
