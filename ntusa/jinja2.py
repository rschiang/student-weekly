import django
import jinja2

def environment(**options):
    env = jinja2.Environment(**options)
    env.globals.update({
        'static': django.contrib.staticfiles.storage.staticfiles_storage.url,
        'url': django.core.urlresolvers.reverse,
    })
    return env
