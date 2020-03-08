from django.db import models

# Create your models here.
from smart_bookmarks.search.db import IndexPageManager


class IndexPage(models.Model):
    id = models.AutoField(primary_key=True)
    page = models.OneToOneField('core.Page', on_delete=models.CASCADE, related_name='index_page')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = IndexPageManager()

    class Meta:
        db_table = 'index_page'
