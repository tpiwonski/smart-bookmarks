from celery import shared_task

from smart_bookmarks.search.models import IndexPage
from smart_bookmarks.search.services import IndexBookmarkService


@shared_task(bind=True)
def index_pages(self):
    pages = IndexPage.objects.pages_to_index()
    for page in pages:
        index_page.delay(page_id=page.id)


@shared_task(bind=True)
def index_page(self, page_id):
    IndexBookmarkService().index_page_by_id(page_id)
