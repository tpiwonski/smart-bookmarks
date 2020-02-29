from django.db import models

from smart_bookmarks.scrapers.db import ScrapePageTaskManager


class ScrapePageTask(models.Model):
    STATE_WAITING = 0
    STATE_PROCESSING = 1
    STATE_FAILED = 2

    STATES = [
        (STATE_WAITING, STATE_WAITING),
        (STATE_PROCESSING, STATE_PROCESSING),
        (STATE_FAILED, STATE_FAILED)
    ]

    id = models.AutoField(primary_key=True)
    bookmark = models.OneToOneField('bookmarks.Bookmark', on_delete=models.CASCADE, related_name='scrape_page_tasks')
    state = models.PositiveSmallIntegerField(choices=STATES, default=STATE_WAITING)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ScrapePageTaskManager()

    class Meta:
        db_table = 'scrape_page_task'

    def update_state(self, state):
        self.state = ScrapePageTask.STATE_FAILED
        self.save(update_fields=['updated', 'state'])
