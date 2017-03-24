from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.views.generic import DetailView, ListView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from issues.forms import ArticleForm, CreateIssueForm
from issues.models import Article, Column, Issue, Provider
from issues.renderers import IssueRenderer
from templates.models import Template

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

    def form_invalid(self, form):
        return redirect('issues:list')

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
            return render(request, 'blank.html')

        is_email = ('email' in request.GET)
        renderer = IssueRenderer(request, issue, is_email=is_email)
        content = renderer.render()

        if is_email:
            return HttpResponse(content, content_type='text/plain; charset=utf-8')
        else:
            return HttpResponse(content)


class IssueEdit(LoginRequiredMixin, DetailView):
    model = Issue
    context_object_name = 'issue'
    template_name = 'issue.html'

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result['columns'] = Column.objects.all()
        result['providers'] = Provider.objects.all()
        return result

    def render_article_data(self, request, article):
        return JsonResponse({
            'name': article.name, 'content': article.content, 'url': article.url,
            'image': article.image.url if article.image else '/assets/placeholder.png',
            'column': article.column.id,
            'provider': article.provider.id if article.provider else None,
        })

    def post(self, request, pk):
        issue = self.get_object()
        if not issue.template:
            if request.POST.get('action') == 'unlock':
                issue.template = Template.objects.first()
                issue.save()
            return redirect('issues:edit', pk=pk)

        article = None
        if 'article_id' in request.POST:
            article = get_object_or_404(Article, pk=request.POST['article_id'])
            if request.is_ajax():
                return self.render_article_data(request, article)

        form = ArticleForm(request.POST, files=request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('issues:edit', pk=pk)

        return JsonResponse(form.errors)
