from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.views.generic import ListView, TemplateView
from issues.forms import ProviderForm
from issues.models import Issue, Provider
from .forms import HintedAuthenticationForm

class Home(ListView):
    context_object_name = 'issue_list'
    template_name = 'weekly/home.html'

    def get_queryset(self):
        cur_date = now().date()
        return Issue.objects.filter(pub_date__lte=cur_date).order_by('-id')


class Settings(LoginRequiredMixin, TemplateView):
    template_name = 'settings.html'

    def get_context_data(self, **kwargs):
        context = super(Settings, self).get_context_data(**kwargs)
        context.update({
            'provider_list': Provider.objects.exclude(description__exact=''),
        })
        return context

    def post(self, request):
        form = ProviderForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
        return redirect('settings')


def login(request):
    return auth.views.login(request,
                            template_name='login.html',
                            authentication_form=HintedAuthenticationForm)


def logout(request):
    return auth.views.logout(request,
                             next_page=reverse_lazy('home'))

def page_not_found(request):
    return render(request, '404.html')

def permission_denied(request):
    return render(request, '403.html')
