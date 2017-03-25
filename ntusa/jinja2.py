import itertools
import jinja2
from django.conf import settings
from django.contrib.staticfiles import storage
from django.core import urlresolvers
from django.utils.timezone import now

def __url(viewname, *args, **kwargs):
    return urlresolvers.reverse(viewname, args=args, kwargs=kwargs)

def __lazy_groupby(iterable, key_name):
    return itertools.groupby(iterable, lambda i: i.__dict__[key_name])

def environment(**options):
    env = jinja2.Environment(**options)
    env.globals.update({
        'meta': settings.SITE_META,
        'now': now,
        'static': storage.staticfiles_storage.url,
        'url': __url,
    })
    env.filters.update({
        'lazy_groupby': __lazy_groupby,
    })
    return env
