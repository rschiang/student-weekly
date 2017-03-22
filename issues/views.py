import os
import pystache
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.utils.timezone import now
from django.views.generic import View, ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from issues.forms import CreateIssueForm
from issues.models import Issue, Column
from itertools import groupby

class IssueList(LoginRequiredMixin, FormMixin, ListView):
    # ListView parameters
    queryset = Issue.objects.order_by('-id')
    context_object_name = 'issue_list'
    template_name = 'issues.html'

    # FormMixin parameters
    form_class = CreateIssueForm

    def get_initial(self):
        return { 'pub_date': now().date() }

    def form_valid(self, form):
        issue = form.save()
        return redirect('issues:edit', pk=issue.id)

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class IssueView(SingleObjectMixin, View):
    model = Issue

    def get(self, request, pk):
        issue = self.get_object()
        if not request.user.is_authenticated and issue.pub_date > now():
            raise Http404   # Hide the existence of unpublished issue

        if not issue.template:
            return HttpResponse('No preview available')

        template_path = issue.template.path
        base_dir = os.path.dirname(template_path)
        base_url = request.build_absolute_uri(settings.THEME_URL + os.path.basename(base_dir))
        renderer = pystache.Renderer(search_dirs=[base_dir])
        context = {
            'issue': issue.id,
            'date': issue.pub_date.strftime('%Y/%m/%d'),
            'path': base_url,
            'email': False,
        }

        articles = issue.articles.select_related('column').order_by('column__position', 'column__id', 'id')
        for col, items in groupby(articles, key=lambda i: i.column):
            if col.layout not in context:
                context[col.layout] = []
            context[col.layout].append({
                'name': col.name,
                'description': col.description,
                'item': list(items),
            })

        return HttpResponse(renderer.render_path(template_path, context))


class IssueEdit(LoginRequiredMixin, DetailView):
    model = Issue
    context_object_name = 'issue'
    template_name = 'issue.html'

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result['columns'] = Column.objects.all()
        return result
