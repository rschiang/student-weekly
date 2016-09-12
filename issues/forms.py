from django.forms import ModelForm
from issues.models import Issue
from templates.models import Template

class CreateIssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['pub_date', 'template']

    def get_templates(self):
        return Template.objects.all()

    def get_next_issue_id(self):
        issue = Issue.objects.order_by('-id').first()
        return (issue.id + 1 if issue else 1)
