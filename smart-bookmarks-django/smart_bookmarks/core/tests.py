from django.test import TestCase
from urllib.parse import urlparse

# Create your tests here.
from smart_bookmarks.core.utils import url_guid


def test_foo():
    guid = url_guid("https://stackoverflow.com/questions/3278077/difference-between-getattr-vs-getattribute/3278104?q=alamakota#1234567")
    print(guid)
