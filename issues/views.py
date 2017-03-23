import os
import pystache
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from django.views.generic import DetailView, ListView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from issues.forms import ArticleForm, CreateIssueForm
from issues.models import Article, Column, Issue, Provider
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
            'email': 'email' in request.GET,
        }

        articles = issue.articles.select_related('column').order_by('column__position', 'column__id', 'id')
        for col, items in groupby(articles, key=lambda i: i.column):
            if col.layout not in context:
                context[col.layout] = []
            context[col.layout].append({
                'name': col.name,
                'description': col.description,
                'item': list({
                    'name': item.name,
                    'url': item.url,
                    'content': item.content,
                    'image_url': request.build_absolute_uri(item.image.url) if item.image else None,
                    'provider_name': item.provider.name if item.provider else None,
                    'provider_icon': request.build_absolute_uri(item.provider.icon.url) if item.provider and item.provider.icon else None,
                } for item in items),
            })

        content_type = 'text/plain; charset=utf-8' if 'email' in request.GET else None
        return HttpResponse(renderer.render_path(template_path, context), content_type=content_type)


class IssueEdit(LoginRequiredMixin, DetailView):
    model = Issue
    context_object_name = 'issue'
    template_name = 'issue.html'

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result['columns'] = Column.objects.all()
        result['providers'] = Provider.objects.all()
        return result

    def post(self, request, pk):
        if 'article_id' in request.POST:
            article = get_object_or_404(Article, pk=request.POST['article_id'])
            if request.is_ajax():
                return JsonResponse({
                    'name': article.name, 'content': article.content, 'url': article.url,
                    'image': article.image.url if article.image else None,
                    'column': article.column.id,
                    'provider': article.provider.id if article.provider else None,
                })
        else:
            article = None

        form = ArticleForm(request.POST, files=request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('issues:edit', pk=pk)
        return JsonResponse(form.errors)
