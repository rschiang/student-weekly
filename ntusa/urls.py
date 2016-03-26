"""NTUSA Weekly Site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import auth
from django.core.urlresolvers import reverse_lazy
from .views import Home, Settings

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'^login/$', auth.views.login, {
            'template_name': 'login.html',
        }),
    url(r'^logout/$', auth.views.logout, {
            'next_page': reverse_lazy('home'),
        }),
    url(r'^settings/$', Settings.as_view(), name='settings'),
    url(r'^issue/', include('issues.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
