import jinja2
from django.conf import settings
from django.contrib.staticfiles import storage
from django.core import urlresolvers

def __url(viewname, *args, **kwargs):
    return urlresolvers.reverse(viewname, args=args, kwargs=kwargs)

def environment(**options):
    env = jinja2.Environment(**options)
    env.globals.update({
        'meta': settings.SITE_META,
        'static': storage.staticfiles_storage.url,
        'url': __url,
    })
    return env
