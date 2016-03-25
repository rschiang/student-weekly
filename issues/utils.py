import base64
import os
from django.utils.timezone import now
from slugify import slugify

def short_id():
    return str(base64.urlsafe_b64encode(os.urandom(6)), 'ascii')

def article_image_url(instance, filename):
    name, _, ext = filename.rpartition('.')
    return '{date:%Y}/{date:%m}/{id}-{name}{dot}{ext}'.format(
        date=now(),
        id=short_id(),
        name=slugify(name, max_length=40),
        dot=_,
        ext=slugify(ext, max_length=10)
    )
