from django.db import models, transaction


class ScrapePageTaskManager(models.Manager):

    @transaction.atomic
    def tasks_to_process(self, limit=10):
        tasks = (
            self.get_queryset().
            select_for_update().
            filter(state=self.model.STATE_WAITING).
            order_by('-created')[:limit])

        for task in tasks:
            task.state = self.model.STATE_PROCESSING

        self.get_queryset().bulk_update(tasks, ['state'])
        return tasks
