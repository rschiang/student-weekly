import json
import os.path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from templates.models import Template

class Command(BaseCommand):
    help = 'Add the specified template to database'

    def add_arguments(self, parser):
        parser.add_argument('template_name')

    def handle(self, *args, **options):
        template_name = options['template_name']
        try:
            meta_path = os.path.join(settings.THEME_ROOT, template_name, 'theme.json')
            with open(meta_path, 'r') as f:
                meta = json.load(f)
        except ValueError:
            raise CommandError('theme.json incorrectly formatted')
        except FileNotFoundError:
            raise CommandError('theme.json does not exist for template “%s”' % template_name)

        template_path = os.path.join(settings.THEME_ROOT, template_name, 'theme.mustache')
        if not os.path.exists(template_path):
            raise CommandError('theme.mustache does not exist for template “%s”' % template_name)

        template = Template()
        template.name = meta.get('name', template_name)
        template.author = meta.get('author', 'N/A')
        template.description = meta.get('description', '')
        template.thumbnail = meta.get('thumbnail', '')
        template.path = template_path
        template.save()

        self.stdout.write(self.style.SUCCESS('Successfully add new template (#%s)' % template.id))
