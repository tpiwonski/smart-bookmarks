import logging

from celery import shared_task, Task
from django.conf import settings

from smart_bookmarks.core.utils import service_instance
from smart_bookmarks.search.models import IndexPage


@shared_task(bind=True)
def index_pages(self):
    pages = IndexPage.objects.pages_to_index()
    for page in pages:
        index_page.delay(page_id=page.id)


@shared_task(bind=True)
def index_page(self, page_id):
    index_service = service_instance(settings.INDEX_SERVICE)
    index_service.index_page_by_id(page_id)
