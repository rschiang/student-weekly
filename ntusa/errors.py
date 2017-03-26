from django.conf.urls import url
from django.shortcuts import render

def page_not_found(request):
    return render(request, '404.html', status=404)

def permission_denied(request):
    return render(request, '403.html', status=403)

def server_error(request):
    return render(request, '500.html', status=500)


urlpatterns = [
    url(r'^404/$', page_not_found),
    url(r'^403/$', permission_denied),
    url(r'^500/$', server_error),
]
