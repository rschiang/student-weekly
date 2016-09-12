from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.utils.timezone import now
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from issues.forms import CreateIssueForm
from issues.models import Issue

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


class IssueView(SingleObjectMixin, View):
    model = Issue

    def get(self, request):
        issue = self.get_object()
        if not request.user.is_authenticated and issue.pub_date > now():
            raise Http404   # Hide the existence of unpublished issue

        return HttpResponse('Wow, such issue %s' % issue.id)    # TODO: Render issue


class IssueEdit(LoginRequiredMixin, DetailView):
    model = Issue
    context_object_name = 'issue'
    template_name = 'issue.html'
