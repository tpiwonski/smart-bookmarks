# Register your models here.
from django.contrib import admin

from smart_bookmarks.core.models import Bookmark, Page

admin.site.register([Bookmark, Page])
