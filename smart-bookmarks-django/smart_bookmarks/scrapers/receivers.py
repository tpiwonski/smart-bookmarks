from django.conf import settings
from django.dispatch import receiver

from smart_bookmarks.core.signals import bookmark_created
from smart_bookmarks.core.utils import event_instance, service_instance


@receiver(bookmark_created, dispatch_uid='smart_bookmarks.scrapers.receivers.on_bookmark_created')
def on_bookmark_created(sender, bookmark, **kwargs):
    scraper_service = service_instance(settings.SCRAPER_SERVICE)
    scraper_service.scrape_page_async(bookmark)
