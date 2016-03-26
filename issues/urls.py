from django.conf.urls import url
from .views import IssueList

app_name = 'issues'
urlpatterns = [
    url(r'^$', IssueList.as_view(), name='list'),
]
