from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.utils.timezone import now
from .models import Issue

class IssueList(LoginRequiredMixin, ListView):
    queryset = Issue.objects.order_by('-id')
    context_object_name = 'issue_list'
    template_name = 'issues.html'

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
