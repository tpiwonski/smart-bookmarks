from django.db import models, transaction


class IndexPageManager(models.Manager):

    @transaction.atomic
    def pages_to_index(self, limit=10):
        index_pages = (
            self.get_queryset().
            select_for_update().
            order_by('created')[:limit])

        pages = [index_page.page for index_page in index_pages]
        self.get_queryset().filter(id__in=index_pages).delete()
        return pages
