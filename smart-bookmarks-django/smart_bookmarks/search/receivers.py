from django.conf import settings
from django.dispatch import receiver

from smart_bookmarks.core.signals import page_created
from smart_bookmarks.core.utils import event_instance, service_instance


@receiver(page_created, dispatch_uid='smart_bookmarks.search.receivers.on_page_created')
def on_page_created(sender, page, **kwargs):
    index_service = service_instance(settings.INDEX_SERVICE)
    index_service.index_page_async(page)
