from django.conf import settings
from django.db import models

class Template(models.Model):
    # Fields
    name = models.CharField(max_length=32, help_text='範本名稱')
    author = models.CharField(max_length=32, help_text='範本作者')
    description = models.TextField(blank=True, help_text='範本說明文字')
    thumbnail = models.URLField(blank=True, max_length=256, help_text='範本預覽縮圖')
    path = models.FilePathField(path=settings.THEME_ROOT, match=r'\.mustache$', recursive=True, max_length=128, help_text='範本檔案位置')

    # Methods
    def __str__(self):
        return '{} [{}]'.format(self.name, self.author)


class Layout(models.Model):
    # Fields
    name = models.CharField(max_length=32, help_text='版型名稱')
    identifier = models.SlugField(max_length=32, db_index=False, help_text='版型識別碼')

    # Related fields
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='layouts')

    # Methods
    def __str__(self):
        return '{} [{}]'.format(self.name, self.identifier)
