from django.forms import DateInput, ModelForm, ValidationError
from issues.models import Article, Issue, Provider
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

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'content', 'image', 'url', 'issue', 'provider', 'column']

class ProviderForm(ModelForm):
    class Meta:
        model = Provider
        fields = ['name', 'description', 'icon', 'site_url']

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('site_url'):
            raise ValidationError('All manually created provider requires site URL.')
        elif not cleaned_data.get('description'):
            raise ValidationError('All manually created provider requires description.')
