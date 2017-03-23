# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-03-23 10:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='column',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='columns', to='issues.Column'),
        ),
        migrations.AlterField(
            model_name='article',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='issues.Issue'),
        ),
        migrations.AlterField(
            model_name='article',
            name='provider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='issues.Provider'),
        ),
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.URLField(blank=True, help_text='文章連結網址', max_length=512),
        ),
        migrations.AlterField(
            model_name='issue',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='issues', to='templates.Template'),
        ),
    ]
