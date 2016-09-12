from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from django.utils.timezone import now
from issues.models import Issue
from templates.models import Template

class IssueList(LoginRequiredMixin, FormMixin, ListView):
    queryset = Issue.objects.order_by('-id')
    context_object_name = 'issue_list'
    template_name = 'issues.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template_list'] = Template.objects.all()
        context['next_issue_id'] = (context['issue_list'][0].id + 1) if context['issue_list'] else 1
        context['now'] = now()
        return context

    def post(self, request):
        pass    # TODO: Create new issue

class IssueView(SingleObjectMixin, View):
    model = Issue

    def get(self, request):
        issue = self.get_object()
        if not request.user.is_authenticated and issue.pub_date > now():
            raise Http404   # Hide the existence of unpublished issue

        return HttpResponse('Wow, such issue %s' % issue.id)

class IssueEdit(LoginRequiredMixin, DetailView):
    model = Issue
    context_object_name = 'issue'
    template_name = 'issue.html'
