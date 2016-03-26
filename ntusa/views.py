from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from templates.models import Template
from issues.models import Issue, Column

class Home(ListView):
    queryset = Issue.objects.order_by('-id')
    context_object_name = 'issue_list'
    template_name = 'home.html'

class Settings(LoginRequiredMixin, TemplateView):
    template_name = 'settings.html'

    def get_context_data(self, **kwargs):
        context = super(Settings, self).get_context_data(**kwargs)
        context.update({
            'column_list': Column.objects.all(),
            'template_list': Template.objects.all(),
        })
        return context
