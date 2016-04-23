from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, TemplateView
from templates.models import Template
from issues.models import Issue, Column
from .forms import HintedAuthenticationForm

class Home(ListView):
    context_object_name = 'issue_list'
    template_name = 'weekly/home.html'

    def get_queryset(self):
        cur_date = now().date()
        return Issue.objects.filter(pub_date__gte=cur_date).order_by('-id')


class Settings(LoginRequiredMixin, TemplateView):
    template_name = 'settings.html'

    def get_context_data(self, **kwargs):
        context = super(Settings, self).get_context_data(**kwargs)
        context.update({
            'column_list': Column.objects.all(),
            'template_list': Template.objects.all(),
        })
        return context


def login(request):
    return auth.views.login(request,
                            template_name='login.html',
                            authentication_form=HintedAuthenticationForm)


def logout(request):
    return auth.views.logout(request,
                             next_page=reverse_lazy('home'))
