from django.contrib import admin

# Register your models here.
from smart_bookmarks.scrapers.models import ScrapePage

admin.site.register([ScrapePage])
