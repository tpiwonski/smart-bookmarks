from django.contrib import admin

# Register your models here.
from smart_bookmarks.bookmarks.models import Bookmark, Page

admin.site.register([Bookmark, Page])
