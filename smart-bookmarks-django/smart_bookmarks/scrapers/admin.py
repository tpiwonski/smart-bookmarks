# Register your models here.
from django.contrib import admin

from smart_bookmarks.scrapers.models import ScrapePageTask

admin.site.register([ScrapePageTask])
