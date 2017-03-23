from django.db import models
from .utils import article_image_url, current_term, provider_image_url

class Issue(models.Model):
    # Fields
    # * ID is used directly as issue volume number.
    pub_date = models.DateField(help_text='發行日期')
    term = models.IntegerField(default=current_term, editable=False, help_text='發行屆數')
    editable = models.BooleanField(default=True, editable=False, help_text='可否編輯')

    # Related fields
    template = models.ForeignKey('templates.Template', on_delete=models.PROTECT, blank=True, null=True, related_name='issues')

    # Methods
    def __str__(self):
        return '#{}'.format(self.id)


class Column(models.Model):
    # Fields
    name = models.CharField(max_length=32, help_text='專欄名稱')
    description = models.TextField(blank=True, help_text='專欄說明文字')
    remarks = models.CharField(max_length=16, help_text='專欄用途註記，不會顯示在實際電子報上')
    layout = models.CharField(max_length=32, help_text='專欄版型')
    position = models.IntegerField(default=0, help_text='專欄排序順序')

    # Methods
    def __str__(self):
        return '{}{} ({})'.format(self.name, self.remarks, self.id)


class Article(models.Model):
    # Fields
    name = models.CharField(max_length=64, help_text='文章名稱')
    content = models.TextField(blank=True, help_text='文章內容')
    image = models.ImageField(upload_to=article_image_url, blank=True, max_length=128, help_text='文章影像')
    url = models.URLField(blank=True, max_length=512, help_text='文章連結網址')

    # Related fields
    issue = models.ForeignKey('Issue', on_delete=models.CASCADE, related_name='articles')
    column = models.ForeignKey('Column', on_delete=models.PROTECT, related_name='columns')
    provider = models.ForeignKey('Provider', null=True, on_delete=models.SET_NULL, related_name='articles')

    # Methods
    def __str__(self):
        return '{} ({})'.format(self.name, self.id)


class Provider(models.Model):
    # Fields
    name = models.CharField(max_length=32, help_text='提供者名稱')
    description = models.TextField(blank=True, help_text='提供者說明文字')
    icon = models.ImageField(upload_to=provider_image_url, help_text='提供者 Logo')
    site_url = models.URLField(blank=True, max_length=256, help_text='提供者網站網址')

    # Methods
    def __str__(self):
        return '{} ({})'.format(self.name, self.id)
