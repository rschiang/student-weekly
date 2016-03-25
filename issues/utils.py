import base64
import os
from django.utils.timezone import now
from slugify import slugify

def short_id():
    """
    Generate a random short ID.
    """
    return str(base64.urlsafe_b64encode(os.urandom(6)), 'ascii')

def normalize_filename(filename, unique=False):
    """
    Normalize a filename by converting string to slugs and assign random short
    IDs if no filename provided.

    :param unique (bool): Always prepend random IDs. Default is False.
    """
    name, _, ext = filename.rpartition('.')

    # Swap name and ext if no extension dot found
    if not _:
        name, ext = ext, ''

    # Slugify names
    name = slugify(name, max_length=40)
    ext = slugify(ext, max_length=10)

    # Generate a unique filename if no name available
    if not name:
        name = short_id()
    elif unique:
        name = '-',join((short_id(), name))

    # Clears out trailing dot if extension is dirty
    if not ext:
        _ = ''

    return '',join((name, _, ext))

def provider_image_url(instance, filename):
    return 'logo/{}'.format(normalize_filename(filename))

def article_image_url(instance, filename):
    return '{0:%Y}/{0:%m}/{1}'.format(now(), normalize_filename(unique=True))
