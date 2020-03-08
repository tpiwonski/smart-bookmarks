import django.dispatch

bookmark_created = django.dispatch.Signal(providing_args=["bookmark"])
page_created = django.dispatch.Signal(providing_args=["page"])
