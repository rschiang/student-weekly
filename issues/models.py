from django.db import models
from .utils import article_image_url, provider_image_url

class Issue(models.Model):
    # Fields
    # * ID is used directly as issue volume number.
    pub_date = models.DateField(help_text='發行日期')

    # Methods
    def __str__(self):
        return '<Issue #{}>'.format(self.id)


class Column(models.Model):
    # Fields
    name = models.CharField(max_length=32, help_text='專欄名稱')
    description = models.TextField(blank=True, help_text='專欄說明文字')
    remarks = models.CharField(max_length=16, help_text='專欄用途註記，不會顯示在實際電子報上')
    layout = models.CharField(max_length=32, help_text='專欄版型')
    position = models.IntegerField(default=0, help_text='專欄排序順序')

    # Methods
    def __str__(self):
        return '<Column {}{}({})>'.format(self.name, self.remarks, self.id)


class Provider(models.Model):
    # Fields
    name = models.CharField(max_length=32, help_text='提供者名稱')
    description = models.TextField(blank=True, help_text='提供者說明')
    image = models.ImageField(upload_to=provider_image_url, help_text='提供者 Logo')
    url = models.URLField(blank=True, max_length=256, help_text='提供者網址')

    # Methods
    def __str__(self):
        return '<Provider {}({})>'.format(self.name, self.id)


class Article(models.Model):
    # Fields
    name = models.CharField(max_length=64, help_text='文章名稱')
    description = models.TextField(blank=True, help_text='文章內容')
    image = models.ImageField(upload_to=article_image_url, blank=True, max_length=128, help_text='文章影像')
    url = models.URLField(blank=True, max_length=256, help_text='文章連結網址')

    # Related fields
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    column = models.ForeignKey(Column, on_delete=models.PROTECT)
    provider = models.ForeignKey(Provider, null=True, on_delete=models.SET_NULL)

    # Methods
    def __str__(self):
        return '<Article {}({})>'.format(self.name, self.id)
