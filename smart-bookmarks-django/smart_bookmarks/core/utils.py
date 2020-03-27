import base64
import hashlib
from urllib.parse import urlparse

from django.utils.module_loading import import_string


def url_guid(url):
    result = urlparse(url)
    content = f"{result.netloc}{result.path}".encode("utf-8")
    hash = hashlib.sha256()
    hash.update(content)
    # return base64.b64encode(hash.digest())
    return hash.hexdigest()
