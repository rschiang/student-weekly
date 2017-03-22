from django.conf.urls import url
from .views import IssueList, IssueEdit, IssueView

app_name = 'issues'
urlpatterns = [
    url(r'^$', IssueList.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)/$', IssueView.as_view(), name='view'),
    url(r'^(?P<pk>[0-9]+)/edit/$', IssueEdit.as_view(), name='edit'),
]
