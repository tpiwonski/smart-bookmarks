# Register your models here.
from django.contrib import admin

from smart_bookmarks.search.models import IndexBookmarkTask

admin.site.register([IndexBookmarkTask])
