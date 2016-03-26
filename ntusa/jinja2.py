import jinja2
from django.contrib.staticfiles import storage
from django.core import urlresolvers

def environment(**options):
    env = jinja2.Environment(**options)
    env.globals.update({
        'static': storage.staticfiles_storage.url,
        'url': urlresolvers.reverse,
    })
    return env
