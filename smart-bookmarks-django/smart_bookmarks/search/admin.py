from django.contrib import admin

# Register your models here.
from smart_bookmarks.search.models import IndexBookmarkTask

admin.site.register([IndexBookmarkTask])
