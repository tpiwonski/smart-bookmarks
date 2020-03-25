from django.urls import re_path
from smart_bookmarks.ui import views, ajax

urlpatterns = [
    re_path(r'^add$', views.add_bookmark, name='add-bookmark'),
    re_path(r'^search$', views.search_bookmarks, name='search-bookmarks'),
    re_path(r'^(?P<bookmark_guid>[0-9a-zA-Z]{64})$', views.show_bookmark, name='show-bookmark'),
    re_path(r'^$', views.list_bookmarks, name='list-bookmarks'),

    re_path(r'^ajax/bookmark/(?P<bookmark_guid>[0-9a-zA-Z]{64})/scrape', ajax.scrape_bookmark, name='ajax-scrape-bookmark'),
    re_path(r'^ajax/bookmark/(?P<bookmark_guid>[0-9a-zA-Z]{64})', ajax.delete_bookmark, name='ajax-handle-bookmark'),
]
