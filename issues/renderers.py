import os
import pystache
from django.conf import settings
from itertools import groupby

class IssueRenderer(object):
    def __init__(self, request, issue, is_email=False):
        self.issue = issue
        self.template_path = issue.template.path
        self.base_dir = os.path.dirname(self.template_path)
        self.base_url = request.build_absolute_uri(settings.THEME_URL + os.path.basename(self.base_dir))
        self.build_absolute_uri = lambda x: request.build_absolute_uri(x)
        self.renderer = pystache.Renderer(search_dirs=[self.base_dir])
        self.is_email = is_email

    def render(self):
        context = {
            'issue': self.issue.id,
            'date': self.issue.pub_date.strftime('%Y/%m/%d'),
            'path': self.base_url,
            'email': self.is_email,
        }

        articles = self.issue.articles.select_related('column').order_by('column__position', 'column__id', 'id')
        for col, items in groupby(articles, key=lambda i: i.column):
            if col.layout not in context:
                context[col.layout] = []
            context[col.layout].append({
                'name': col.name,
                'description': col.description,
                'item': list(self.render_article(item) for item in items),
            })

        return self.renderer.render_path(self.template_path, context)

    def render_article(self, item):
        context = {
            'name': item.name,
            'url': item.url,
            'content': item.content,
            'image_url': self.build_absolute_uri(item.image.url if item.image else '/assets/placeholder-large.png'),
        }

        provider = item.provider
        if provider:
            context['provider_name'] = provider.name
            if provider.icon:
                context['provider_icon'] = self.build_absolute_uri(provider.icon.url)

        return context

    def render_to_file(self):
        path = os.path.join(settings.RENDERED_ISSUE_ROOT, '{}.html'.format(self.issue.id))
        with open(path, 'w+') as f:
            f.write(self.render())
