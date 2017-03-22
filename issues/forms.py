from django.forms import ModelForm, DateInput
from issues.models import Issue
from templates.models import Template

class CreateIssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['pub_date', 'template']
        widgets = {
            'pub_date': DateInput(format='%Y-%m-%d'),
        }

    def get_templates(self):
        return Template.objects.all()

    def get_next_issue_id(self):
        issue = Issue.objects.order_by('-id').first()
        return (issue.id + 1 if issue else 1)
