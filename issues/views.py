from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Issue

class IssueList(LoginRequiredMixin, ListView):
    queryset = Issue.objects.order_by('-id')
    context_object_name = 'issue_list'
    template_name = 'issues.html'
